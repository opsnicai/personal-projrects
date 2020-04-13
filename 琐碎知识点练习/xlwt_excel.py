import xlwt

path = r"test.xls"

# 规定编码和样式
book = xlwt.Workbook(encoding="utf-8", style_compression=0)

# 表名 和 不允许单元格覆盖
sheet = book.add_sheet("test", cell_overwrite_ok=False)
sheet.write(0,0,"ahhh")
#
# # 行 列 ，都从 0 开始
# sheet.write(9,8,"test")


# 九九乘法表
for i in range(1, 10):
    for j in range(1, i + 1):
        sheet.write(i - 1, j - 1 , "%s * %s = %s" % (j, i, i * j,))


book.save(path)
