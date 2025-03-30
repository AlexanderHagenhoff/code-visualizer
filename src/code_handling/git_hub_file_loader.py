import requests
import re
import fnmatch
from typing import List, Optional
from pathlib import Path
from src.code_handling.code_provider import CodeProvider
from src.code_handling.code_file import CodeFile


class GitHubFileLoader(CodeProvider):
    GITHUB_API_URL = "https://api.github.com"
    GITHUB_RAW_URL = "https://raw.githubusercontent.com"

    def __init__(self, token: Optional[str] = None):
        self.token = token
        self.session = requests.Session()
        if token:
            self.session.headers.update({"Authorization": f"token {token}"})

    def load_code_files(
            self,
            urls: List[str],
            file_pattern: List[str],
            ignore_patterns: List[str] = None
    ) -> List[CodeFile]:
        ignore_patterns = ignore_patterns or []
        code_files = []
        for url in urls:
            if 'github.com' not in url:
                continue

            if '/blob/' in url:
                if not self._is_ignored(url, ignore_patterns):
                    code_files.append(self._load_single_file(url, file_pattern))
            else:
                repo_info = self._extract_repo_info(url)
                if repo_info:
                    code_files.extend(self._scan_repository(
                        owner=repo_info['owner'],
                        repo=repo_info['repo'],
                        path=repo_info.get('path', ''),
                        file_pattern=file_pattern,
                        ignore_patterns=ignore_patterns
                    ))
        return code_files

    def _load_single_file(self, file_url: str, file_pattern: List[str]) -> CodeFile:
        filename = Path(file_url).name
        if not self._matches_pattern(filename, file_pattern):
            return CodeFile(content="", filename=filename)

        raw_url = file_url.replace('github.com', self.GITHUB_RAW_URL).replace('/blob/', '/')
        response = self.session.get(raw_url)
        response.raise_for_status()
        return CodeFile(content=response.text, filename=filename)

    def _extract_repo_info(self, url: str) -> Optional[dict]:
        pattern = r"github\.com/([^/]+)/([^/]+)(/tree/[^/]+/(.*))?"
        match = re.search(pattern, url)
        if match:
            return {
                'owner': match.group(1),
                'repo': match.group(2),
                'path': match.group(4) if match.group(4) else ''
            }
        return None

    def _scan_repository(
            self,
            owner: str,
            repo: str,
            path: str,
            file_pattern: List[str],
            ignore_patterns: List[str]
    ) -> List[CodeFile]:
        api_url = f"{self.GITHUB_API_URL}/repos/{owner}/{repo}/contents/{path}"
        response = self.session.get(api_url)
        response.raise_for_status()

        code_files = []
        for item in response.json():
            item_path = item['path']
            if self._is_ignored(item_path, ignore_patterns):
                continue

            if item['type'] == 'file':
                if self._matches_pattern(item['name'], file_pattern):
                    file_content = self.session.get(item['download_url']).text
                    code_files.append(CodeFile(content=file_content, filename=item_path))

            elif item['type'] == 'dir':
                code_files.extend(self._scan_repository(
                    owner=owner,
                    repo=repo,
                    path=item_path,
                    file_pattern=file_pattern,
                    ignore_patterns=ignore_patterns
                ))

        return code_files

    def _is_ignored(self, path: str, patterns: List[str]) -> bool:
        return any(
            fnmatch.fnmatch(path, pattern) or
            fnmatch.fnmatch(Path(path).name, pattern)
            for pattern in patterns
        )

    def _matches_pattern(self, filename: str, patterns: List[str]) -> bool:
        return any(fnmatch.fnmatch(filename, pattern) for pattern in patterns)
