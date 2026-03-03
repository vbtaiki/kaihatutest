#!/usr/bin/env python3
"""
VB-OS Dashboard Builder
Markdownファイルから自動的にダッシュボード用のJSONデータを生成します。
"""

import os
import re
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

class MarkdownParser:
    """Markdownファイルを解析してデータを抽出"""

    @staticmethod
    def extract_section(content: str, section_title: str) -> str:
        """特定のセクションの内容を抽出"""
        pattern = rf'## {re.escape(section_title)}\s*\n(.*?)(?=\n## |\Z)'
        match = re.search(pattern, content, re.DOTALL)
        return match.group(1).strip() if match else ""

    @staticmethod
    def extract_blockquote(content: str) -> str:
        """引用ブロック（> で始まる行）を抽出"""
        lines = content.split('\n')
        quote_lines = [line.lstrip('> ').strip() for line in lines if line.strip().startswith('>')]
        return ' '.join(quote_lines)

    @staticmethod
    def extract_table_data(content: str) -> List[Dict[str, str]]:
        """Markdownテーブルをパース"""
        lines = [line.strip() for line in content.split('\n') if line.strip() and not line.strip().startswith('|---')]
        if len(lines) < 2:
            return []

        header = [cell.strip() for cell in lines[0].split('|')[1:-1]]
        rows = []
        for line in lines[1:]:
            cells = [cell.strip() for cell in line.split('|')[1:-1]]
            if len(cells) == len(header):
                rows.append(dict(zip(header, cells)))
        return rows

class TeamParser:
    """チームのREADME.mdを解析"""

    def __init__(self, team_dir: Path):
        self.team_dir = team_dir
        self.readme_path = team_dir / 'README.md'

    def parse(self) -> Dict[str, Any]:
        """チーム情報を抽出"""
        if not self.readme_path.exists():
            return None

        with open(self.readme_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # タイトルから名前を抽出
        title_match = re.search(r'# Team: (.+)', content)
        team_name = title_match.group(1) if title_match else self.team_dir.name

        # Founder's Expectationを抽出
        expectation_section = MarkdownParser.extract_section(content, "💭 Founder's Expectation")
        expectation = MarkdownParser.extract_blockquote(expectation_section)

        # ミッションを抽出
        mission_section = MarkdownParser.extract_section(content, "🎯 ミッション")
        mission = mission_section.split('\n')[0] if mission_section else ""

        # メンバーを抽出
        members_section = MarkdownParser.extract_section(content, "👥 Members")
        members = MarkdownParser.extract_table_data(members_section)

        # KPIを抽出
        kpi_section = MarkdownParser.extract_section(content, "📊 KPI")
        kpis = MarkdownParser.extract_table_data(kpi_section)

        # プロジェクトを抽出
        projects = self._extract_projects(content)

        # アイコンを推定
        icon = self._guess_icon(team_name)

        return {
            'id': self.team_dir.name,
            'name': team_name,
            'icon': icon,
            'mission': mission,
            'expectation': expectation,
            'members': members,
            'kpis': kpis,
            'projects': projects
        }

    def _extract_projects(self, content: str) -> List[Dict[str, str]]:
        """プロジェクト情報を抽出"""
        projects = []
        projects_section = MarkdownParser.extract_section(content, "📂 Projects")

        # ### 見出しでプロジェクトを分割
        project_blocks = re.findall(r'### (.+?)\n(.*?)(?=\n### |\Z)', projects_section, re.DOTALL)

        for title, details in project_blocks:
            project = {'name': title.strip()}

            # ファイル情報
            file_match = re.search(r'\*\*ファイル\*\*: `(.+?)`', details)
            if file_match:
                project['file'] = file_match.group(1)

            # 概要
            summary_match = re.search(r'\*\*概要\*\*: (.+)', details)
            if summary_match:
                project['summary'] = summary_match.group(1).strip()

            # ステータス推定（計画中/進行中/完了を検出）
            if '計画' in details or '🟡' in details:
                project['status'] = 'planning'
            elif '完了' in details or '✅' in details:
                project['status'] = 'completed'
            else:
                project['status'] = 'progress'

            projects.append(project)

        return projects

    def _guess_icon(self, team_name: str) -> str:
        """チーム名から適切なアイコンを推定"""
        icon_map = {
            'ガバナンス': '🏛️',
            '倉庫': '🏭',
            '買取': '📦',
            'ロジ': '🚚',
            'Web': '💻',
            'プロアカウント': '🤝',
            'MD': '🤝',
        }

        for keyword, icon in icon_map.items():
            if keyword in team_name:
                return icon
        return '📁'

class MemberParser:
    """メンバーの.mdファイルを解析"""

    def __init__(self, member_file: Path):
        self.member_file = member_file

    def parse(self) -> Dict[str, Any]:
        """メンバー情報を抽出"""
        if not self.member_file.exists():
            return None

        with open(self.member_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # タイトルから名前を抽出
        title_match = re.search(r'# (.+)', content)
        name = title_match.group(1).split('(')[0].strip() if title_match else self.member_file.stem

        # 基本情報テーブルを抽出
        basic_info_section = MarkdownParser.extract_section(content, "基本情報")
        basic_info = MarkdownParser.extract_table_data(basic_info_section)

        # 所属チーム情報を抽出
        team_section = MarkdownParser.extract_section(content, "所属チーム・役割")
        teams = MarkdownParser.extract_table_data(team_section)

        # 担当プロジェクトを抽出
        project_section = MarkdownParser.extract_section(content, "担当プロジェクト")
        projects = MarkdownParser.extract_table_data(project_section)

        result = {
            'id': self.member_file.stem,
            'name': name,
            'teams': teams,
            'projects': projects
        }

        # 基本情報から役職と拠点を抽出
        for info in basic_info:
            if info.get('項目') == '役職':
                result['role'] = info.get('内容', '')
            if info.get('項目') == '拠点':
                result['location'] = info.get('内容', '')

        return result

class DashboardBuilder:
    """ダッシュボード用データを構築"""

    def __init__(self, root_dir: str):
        self.root_dir = Path(root_dir)
        self.teams_dir = self.root_dir / 'teams'
        self.members_dir = self.root_dir / 'members'

    def build(self) -> Dict[str, Any]:
        """全データを構築"""
        data = {
            'meta': {
                'updated_at': datetime.now().isoformat(),
                'version': '1.0.0'
            },
            'teams': self._build_teams(),
            'members': self._build_members()
        }
        return data

    def _build_teams(self) -> List[Dict[str, Any]]:
        """全チームのデータを構築"""
        teams = []

        if not self.teams_dir.exists():
            return teams

        for team_dir in sorted(self.teams_dir.iterdir()):
            if team_dir.is_dir():
                parser = TeamParser(team_dir)
                team_data = parser.parse()
                if team_data:
                    teams.append(team_data)

        return teams

    def _build_members(self) -> List[Dict[str, Any]]:
        """全メンバーのデータを構築"""
        members = []

        if not self.members_dir.exists():
            return members

        for member_file in sorted(self.members_dir.glob('*.md')):
            parser = MemberParser(member_file)
            member_data = parser.parse()
            if member_data:
                members.append(member_data)

        return members

def main():
    """メイン処理"""
    # カレントディレクトリを取得
    root_dir = Path(__file__).parent

    print("🔨 VB-OS Dashboard Builder")
    print(f"📁 Root directory: {root_dir}")
    print()

    # データを構築
    print("📊 Building data from Markdown files...")
    builder = DashboardBuilder(root_dir)
    data = builder.build()

    print(f"✅ Found {len(data['teams'])} teams")
    print(f"✅ Found {len(data['members'])} members")
    print()

    # JSONファイルに出力
    output_dir = root_dir / 'dashboard-v2'
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / 'data.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"💾 Data saved to: {output_file}")
    print(f"📅 Updated at: {data['meta']['updated_at']}")
    print()
    print("✨ Build complete!")

if __name__ == '__main__':
    main()
