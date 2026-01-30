
<div align="center">
  <img src="./assets/MyManus.png" alt="MyManus">
</div>
 
MyManus is the 100% free, 0% coding, **local**, **secure** agentic environment akin to [Manus AI](https://manus.im/) built entirely around Model Context Protocol [MCP](https://modelcontextprotocol.io/introduction) implementation.

MyManus uses sandboxing to secure your system and allow AI agent to use a browser, create files, run commands, and more.

My Manus securely runs the browser on a local machine rather than on some flimsy cloud server, which makes it fast, free, and reliable.

Thanks to its magic [prompt](./prompts/prompt.md), MyManus plans, reasons, executes, evaluates, and deals with all the issues on its own. 

RESEARCH, CODING, DATA ANALYSIS, PRODUCTIVITY, LIFE, you name it. Depending on the set of tools, it can be used for any task you can imagine.

All that you need is [Claude Desktop](https://github.com/emsi/claude-desktop) app (or any other [MCP Client](https://modelcontextprotocol.io/clients)) and a bunch of existing [MCP servers](https://modelcontextprotocol.io/examples) to set up your ultimate agentic environment, allowing the AI agent to do all the tasks you can imagine. No need to write a single line of code. No need to purchase additional software (apart from an existing [claude.ai](https://claude.ai/) subscription or LLM API).

---

# Installation Options

## For Claude Code (Recommended)

MyManus is now available as a plugin for [Claude Code](https://claude.com/claude-code), Anthropic's official CLI!

**[→ Claude Code Installation Guide](./INSTALL_CLAUDECODE.md)**

## For Claude Desktop

To install MyManus for Claude Desktop app:

**[→ Installation Guide (Linux/macOS)](./INSTALL.md)**
**[→ Windows Installation Guide](./WINDOWS_INSTALL.md)**

---

# [USAGE](./USAGE.md)
To use MyManus, follow the [usage guide](./USAGE.md).

# [EXAMPLES](./EXAMPLES.md)

To see MyManus in action, check out the [examples](./EXAMPLES.md).

---

# Skills Marketplace

MyManus now includes a built-in **Skills Marketplace** with 8 professional skills, all in Traditional Chinese:

## 📊 Data & Analysis
- **stock-analysis** (v1.0.0) - Stock and company financial analysis
- **excel-generator** (v1.0.0) - Professional Excel spreadsheet creation
- **similarweb-analytics** (v1.0.0) - Website traffic and engagement analysis

## 🔍 Tool Search
- **github-gem-seeker** (v2.0.0) - Search GitHub for battle-tested solutions and sensitive data
- **internet-skill-finder** (v1.0.0) - Search and recommend Agent Skills

## 🛠️ Development Tools
- **skill-creator** (v1.0.0) - Interactive skill creation guide

## 🔒 Security & Penetration Testing
- **penetration-testing** (v1.0.0) - Integrated penetration testing framework (Shodan + Nmap + Kali Tools)
  - Includes professional **White Hat Hacker Prompt**
  - Deep vulnerability verification
  - Custom code generation when standard tools fail
  - Systematic thinking chain: Observe → Hypothesize → Test → Analyze → Act

All skills are located in `mymanus-plugin/skills/` and are automatically loaded when MyManus starts.

For more information, see [mymanus-plugin/skills/README.md](./mymanus-plugin/skills/README.md).