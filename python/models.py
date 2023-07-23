from tortoise import fields
from tortoise.models import Model


class Users(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(index=True, max_length=32, description="用户名")
    desc = fields.TextField(description="用户描述")
    phone = fields.CharField(unique=True, max_length=15, description="手机号")
    energy = fields.IntField(default=0, description="能量总值")
    available_energy = fields.IntField(default=0, description="可用能量")
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")
    updated_at = fields.DatetimeField(auto_now=True, description="更新时间")

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.id} {self.name}>"


class Trees(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(index=True, max_length=32, description="树名")
    desc = fields.TextField(description="树木描述")
    energy = fields.IntField(default=0, description="购买所需能量")
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")
    updated_at = fields.DatetimeField(auto_now=True, description="更新时间")
    user = fields.ForeignKeyField("models.Users")

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.id}>"

    class Meta:
        ordering = ["-id"]
