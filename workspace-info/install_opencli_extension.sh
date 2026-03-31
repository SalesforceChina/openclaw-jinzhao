#!/bin/bash

echo "🔧 OpenCLI Browser Extension 安装脚本"
echo "======================================"

# 检查是否在/tmp目录
if [ ! -d "/tmp/opencli-extension-new" ]; then
    echo "❌ 扩展文件不存在，正在下载..."
    cd /tmp
    wget -O opencli-extension.zip https://github.com/jackwener/opencli/releases/latest/download/opencli-extension.zip
    unzip -q opencli-extension.zip -d opencli-extension-new
    echo "✅ 扩展文件下载完成"
fi

echo ""
echo "📁 扩展文件位置: /tmp/opencli-extension-new/"
echo ""

echo "📋 文件列表:"
ls -la /tmp/opencli-extension-new/

echo ""
echo "🚀 安装步骤:"
echo "1. 打开Chrome浏览器"
echo "2. 访问: chrome://extensions/"
echo "3. 开启右上角的'开发者模式'"
echo "4. 点击'加载已解压的扩展程序'"
echo "5. 选择目录: /tmp/opencli-extension-new/"
echo "6. 点击'选择文件夹'"
echo ""

echo "🔗 验证安装:"
echo "1. 扩展列表中应该出现 'OpenCLI Browser Bridge'"
echo "2. 扩展图标应该出现在Chrome工具栏中"
echo ""

echo "🧪 测试连接:"
echo "运行以下命令测试:"
echo "  opencli doctor"
echo "  opencli zhihu hot --limit 2 -f json"
echo ""

echo "📝 重要提醒:"
echo "1. 保持Chrome浏览器运行"
echo "2. 在Chrome中登录知乎、Bilibili等平台"
echo "3. 不要关闭Chrome浏览器"
echo ""

echo "🎉 安装完成！现在可以测试完整功能了。"