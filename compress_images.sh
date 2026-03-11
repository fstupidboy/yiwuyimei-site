#!/bin/bash
# 批量压缩网站图片脚本
# 将大于 1MB 的图片压缩到 1200px 宽度

echo "=========================================="
echo "🖼️  网站图片批量压缩工具"
echo "=========================================="
echo ""

STATIC_DIR="/Volumes/ZHITAI2T/kimi2/website_design/www.yiwuyimei.com.backup/static/images"
BACKUP_DIR="/Volumes/ZHITAI2T/kimi2/website_design/www.yiwuyimei.com.backup/images_backup"

# 统计信息
TOTAL_ORIGINAL_SIZE=0
TOTAL_NEW_SIZE=0
COMPRESSED_COUNT=0
SKIPPED_COUNT=0
PNG_TO_WEBP_COUNT=0

START_TIME=$(date +%s)

# 处理所有大于 1MB 的图片
echo "🔍 扫描大于 1MB 的图片..."
echo ""

find "$STATIC_DIR" -type f -size +1M \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" \) | while read img; do
    FILENAME=$(basename "$img")
    DIRNAME=$(dirname "$img")
    EXT="${FILENAME##*.}"
    EXT_LOWER=$(echo "$EXT" | tr '[:upper:]' '[:lower:]')
    
    ORIG_SIZE=$(stat -f%z "$img")
    TOTAL_ORIGINAL_SIZE=$((TOTAL_ORIGINAL_SIZE + ORIG_SIZE))
    
    # 对于 PNG 文件，转换为 WebP
    if [ "$EXT_LOWER" = "png" ]; then
        NEW_FILENAME="${FILENAME%.*}.webp"
        NEW_PATH="$DIRNAME/$NEW_FILENAME"
        
        magick "$img" -resize 1200x1200\> -quality 85 -strip "$NEW_PATH"
        
        if [ -f "$NEW_PATH" ]; then
            rm "$img"  # 删除原 PNG
            NEW_SIZE=$(stat -f%z "$NEW_PATH")
            TOTAL_NEW_SIZE=$((TOTAL_NEW_SIZE + NEW_SIZE))
            COMPRESSED_COUNT=$((COMPRESSED_COUNT + 1))
            PNG_TO_WEBP_COUNT=$((PNG_TO_WEBP_COUNT + 1))
            
            echo "✅ $FILENAME → $NEW_FILENAME ($(($ORIG_SIZE/1024/1024))MB → $(($NEW_SIZE/1024))KB) [PNG→WebP]"
        fi
    else
        # 对于 JPEG 文件，原地压缩
        magick "$img" -resize 1200x1200\> -quality 85 -strip "$img"
        NEW_SIZE=$(stat -f%z "$img")
        TOTAL_NEW_SIZE=$((TOTAL_NEW_SIZE + NEW_SIZE))
        COMPRESSED_COUNT=$((COMPRESSED_COUNT + 1))
        
        echo "✅ $FILENAME ($(($ORIG_SIZE/1024/1024))MB → $(($NEW_SIZE/1024))KB)"
    fi
done

END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

echo ""
echo "=========================================="
echo "📊 压缩报告"
echo "=========================================="
echo "处理图片数: $COMPRESSED_COUNT"
echo "PNG转WebP: $PNG_TO_WEBP_COUNT"
echo "总耗时: ${DURATION}秒"
echo "=========================================="
