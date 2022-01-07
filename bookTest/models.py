from django.db import models


# Create your models here.
class Book(models.Model):
    book_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128, verbose_name="书名", null=True, default=None, help_text="书名")
    desc = models.CharField(max_length=500, verbose_name="书描述", null=True, default=None, help_text="书描述")
    read = models.IntegerField(verbose_name="阅读量", null=True, default=0, help_text="阅读量")
    isSell = models.BooleanField(verbose_name="是否可卖", null=True, default=False, help_text="是否可卖")
    createTime = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="创建时间")

    class Meta:
        # 为这个类定义一个说明
        verbose_name = "书表"
        db_table = "book"
        verbose_name_plural = "书"
