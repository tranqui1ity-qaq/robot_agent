#!/usr/bin/env python3
"""
OpenRouter 模型可用性诊断脚本

用法:
    python diagnose_openrouter.py
"""

import os
import sys
import json
from openai import OpenAI

def main():
    api_key = os.environ.get("OPENROUTER_API_KEY", "")
    if not api_key:
        print("❌ ERROR: OPENROUTER_API_KEY not set!")
        print("   Run: export OPENROUTER_API_KEY='your-key-here'")
        sys.exit(1)
    
    base_url = "https://openrouter.ai/api/v1"
    
    # 创建客户端
    client = OpenAI(api_key=api_key, base_url=base_url)
    client.default_headers["HTTP-Referer"] = "https://github.com/robot_agent"
    client.default_headers["X-Title"] = "Robot Agent Diagnostic"
    
    # 测试的模型列表
    models_to_test = [
        "openai/gpt-3.5-turbo",
        "openai/gpt-4-turbo",
        "anthropic/claude-3.5-sonnet",
        "anthropic/claude-3-opus",
        "mistralai/mistral-large",
        "mistralai/mistral-medium",
        "meta-llama/llama-2-70b-chat",
        "google/gemini-pro",
        "deepseek/deepseek-chat",
    ]
    
    print("=" * 60)
    print("OpenRouter 模型可用性诊断")
    print("=" * 60)
    print(f"\n✓ API Key 已设置")
    print(f"✓ Base URL: {base_url}")
    print(f"\n正在检测可用模型...\n")
    
    available_models = []
    unavailable_models = []
    
    for model in models_to_test:
        sys.stdout.write(f"  测试 {model:<40} ... ")
        sys.stdout.flush()
        
        try:
            # 尝试创建一个简单的请求
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": "test"}],
                temperature=0.0,
                max_tokens=10,
            )
            print("✓ 可用")
            available_models.append(model)
        
        except Exception as e:
            error_msg = str(e)
            if "404" in error_msg:
                print("✗ 404 (不存在)")
            elif "403" in error_msg:
                print("✗ 403 (无权限/地域限制)")
            elif "501" in error_msg:
                print("✗ 501 (模型 offline)")
            else:
                print(f"✗ 错误: {error_msg[:40]}")
            unavailable_models.append((model, error_msg))
    
    # 总结
    print("\n" + "=" * 60)
    print("诊断结果")
    print("=" * 60)
    
    if available_models:
        print(f"\n✓ 可用模型 ({len(available_models)}):")
        for model in available_models:
            print(f"  - {model}")
        
        print("\n💡 建议命令:")
        for model in available_models[:1]:
            print(f"  export LLM_MODEL='{model}'")
            print(f"  python main.py --mode llm --provider openrouter --max-steps 50")
    else:
        print("\n❌ 没有找到可用的模型！")
        print("\n可能原因:")
        print("  1. API Key 无效或已过期")
        print("  2. 账户没有额度或处于限制状态")
        print("  3. 所在地区无法访问这些模型")
        print("  4. 网络连接问题")
        
        print("\n故障排查步骤:")
        print("  1. 访问 https://openrouter.ai/account/billing/overview 检查账户余额")
        print("  2. 访问 https://openrouter.ai/models 查看可用模型")
        print("  3. 尝试在浏览器直接访问 API 测试连接")
        print("  4. 检查是否有 VPN 或代理设置")
    
    print("\n" + "=" * 60)
    print("\n不可用的模型细节:")
    for model, error in unavailable_models[:3]:
        print(f"\n{model}:")
        print(f"  {error[:100]}")
    
    print("\n" + "=" * 60)
    print("更多信息:")
    print("  - 查看所有模型: https://openrouter.ai/models")
    print("  - 官方文档: https://openrouter.ai/docs")
    print("  - 检查账户: https://openrouter.ai/account/billing/overview")
    print("=" * 60)
    
    return 0 if available_models else 1

if __name__ == "__main__":
    sys.exit(main())
