#!/bin/bash
# push-to-github.sh - 一键推送到 GitHub

set -e

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║         推送 robot_agent 项目到 GitHub                        ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# 检查是否提供了 remote URL
if [ -z "$1" ]; then
    echo "❌ 错误：请提供 GitHub remote URL"
    echo ""
    echo "使用方法："
    echo "  ./push-to-github.sh <remote-url>"
    echo ""
    echo "示例："
    echo "  # HTTPS"
    echo "  ./push-to-github.sh https://github.com/YOUR_USERNAME/robot_agent.git"
    echo ""
    echo "  # SSH"
    echo "  ./push-to-github.sh git@github.com:YOUR_USERNAME/robot_agent.git"
    echo ""
    exit 1
fi

REMOTE_URL="$1"

echo "📝 添加远程仓库..."
git remote add origin "$REMOTE_URL"

echo "🔄 推送到 GitHub（main 分支）..."
git push -u origin main

echo ""
echo "✅ 成功！项目已推送到 GitHub！"
echo ""
echo "📊 查看仓库："
echo "  $REMOTE_URL"
echo ""
echo "🔗 后续命令："
echo "  # 查看远程信息"
echo "  git remote -v"
echo ""
echo "  # 查看日志"
echo "  git log --oneline"
echo ""
echo "  # 更新时"
echo "  git add ."
echo "  git commit -m 'Your message'"
echo "  git push"
