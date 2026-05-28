import sys, os
from datetime import datetime

def scaffold(plugin_name, display_name, author, desc):
    dir_name = f"astrbot_plugin_{plugin_name.replace(' ', '_').replace('-', '_').lower()}"
    os.makedirs(dir_name, exist_ok=True)

    # Escape braces for f-strings
    main_py = (
        "import re\n"
        "from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult\n"
        "from astrbot.api.star import Context, Star\n"
        "from astrbot.api import logger\n"
        "\n"
        "class Main(Star):\n"
        "    def __init__(self, context: Context, config: dict = None):\n"
        "        super().__init__(context)\n"
        f'        self.config = config or {{}}\n'
        "\n"
        f"    @filter.command(\"{plugin_name}\")\n"
        f"    async def {plugin_name}_cmd(self, event: AstrMessageEvent):\n"
        "        user_name = event.get_sender_name()\n"
        f'        yield event.plain_result(f"Hello, {{user_name}}! — {display_name}")\n'
        "\n"
        "    @filter.on_decorating_result()\n"
        "    async def on_decorating_result(self, event: AstrMessageEvent):\n"
        "        pass\n"
    )

    metadata = (
        f"name: {plugin_name}\n"
        f"desc: {desc}\n"
        f"help: {display_name} - {desc}\n"
        "version: v1.0.0\n"
        f"author: {author}\n"
        f"repo: https://github.com/{author}/{dir_name}\n"
    )

    conf = (
        "{\n"
        f'  "{plugin_name}_enabled": {{\n'
        f'    "description": "启用 {display_name}",\n'
        '    "type": "bool",\n'
        '    "default": true\n'
        "  }\n"
        "}\n"
    )

    readme = (
        f"# astrbot-plugin-{plugin_name}\n"
        "\n"
        "[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)\n"
        "[![AstrBot](https://img.shields.io/badge/AstrBot-plugin-6c5ce7.svg)](https://github.com/AstrBotDevs/AstrBot)\n"
        "\n"
        f"{display_name} — {desc}\n"
        "\n"
        "## 安装\n\n"
        "```bash\n"
        "cd ~/.astrbot/data/plugins\n"
        f"git clone https://github.com/{author}/{dir_name}.git {plugin_name}\n"
        "```\n\n"
        "## 配置\n\n"
        f"| {plugin_name}_enabled | bool | true | 启用插件 |\n"
        "\n"
        "## 许可证\n\nMIT License\n"
    )

    year = datetime.now().year
    license_text = (
        "MIT License\n\n"
        f"Copyright (c) {year} {author}\n\n"
        "Permission is hereby granted, free of charge, to any person obtaining a copy\n"
        "of this software and associated documentation files (the \"Software\"), to deal\n"
        "in the Software without restriction, including without limitation the rights\n"
        "to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n"
        "copies of the Software, and to permit persons to whom the Software is\n"
        "furnished to do so, subject to the following conditions:\n\n"
        "The above copyright notice and this permission notice shall be included in all\n"
        "copies or substantial portions of the Software.\n\n"
        'THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n'
        "IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n"
        "FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n"
        "AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n"
        "LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n"
        "OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\n"
        "SOFTWARE.\n"
    )

    gattr = "* text=auto eol=lf\n*.py text eol=lf\n*.md text eol=lf diff=markdown\n*.yaml text eol=lf\n*.yml text eol=lf\n*.json text eol=lf\nLICENSE text eol=lf\n"

    for fname, content in [
        ("main.py", main_py),
        ("metadata.yaml", metadata),
        ("_conf_schema.json", conf),
        ("README.md", readme),
        ("LICENSE", license_text),
        (".gitattributes", gattr),
    ]:
        with open(os.path.join(dir_name, fname), "w", encoding="utf-8") as f:
            f.write(content)

    gh_workflow = os.path.join(dir_name, ".github", "workflows")
    os.makedirs(gh_workflow, exist_ok=True)
    release_yml = (
        "name: Release\n"
        "on:\n"
        "  push:\n"
        "    tags:\n"
        "      - 'v*'\n"
        "jobs:\n"
        "  release:\n"
        "    runs-on: ubuntu-latest\n"
        "    permissions:\n"
        "      contents: write\n"
        "    steps:\n"
        "      - uses: actions/checkout@v4\n"
        "      - name: Create Release\n"
        "        uses: softprops/action-gh-release@v2\n"
        "        with:\n"
        f'          name: "{display_name} ${{{{ github.ref_name }}}}"\n'
        "          generate_release_notes: true\n"
        "          files: |\n"
        "            main.py\n"
        "            metadata.yaml\n"
        "            _conf_schema.json\n"
        "            README.md\n"
        "            LICENSE\n"
    )
    with open(os.path.join(gh_workflow, "release.yml"), "w", encoding="utf-8") as f:
        f.write(release_yml)

    print(f"OK: {os.path.abspath(dir_name)}")
    print("Next steps:")
    print(f"  cd {dir_name}")
    print("  git init && git add -A && git commit -m 'init'")
    print(f"  git remote add origin https://github.com/{author}/{dir_name}.git")
    print("  git push -u origin master")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("python scripts/_gen_scaffold.py <name> <display> <author> [desc]")
        sys.exit(1)
    n, d, a = sys.argv[1], sys.argv[2], sys.argv[3]
    desc = sys.argv[4] if len(sys.argv) > 4 else f"{d} 插件"
    scaffold(n, d, a, desc)
