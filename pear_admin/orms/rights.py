from sqlalchemy.orm import backref

from pear_admin.extensions import db

from ._base import BaseORM


class RightsORM(BaseORM):
    __tablename__ = "ums_rights"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, comment="权限名称")
    code = db.Column(db.String(30), comment="权限标识")
    type = db.Column(db.String(30), comment="权限类型")
    url = db.Column(db.String(30), comment="路径地址")

    icon_sign = db.Column(db.String(128), comment="图标")
    status = db.Column(db.Boolean, default=True, comment="是否开启")
    sort = db.Column(db.Integer, default=0)
    open_type = db.Column(db.String(128), comment="打开方式")
    pid = db.Column(
        db.Integer,
        db.ForeignKey("ums_rights.id"),
        default=0,
        comment="父类编号",
    )

    parent = db.relationship(
        "RightsORM", back_populates="children", remote_side=[id]
    )  # 自关联
    children = db.relationship("RightsORM", back_populates="parent")

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "type": self.type,
            "url": self.url,
            "icon_sign": self.icon_sign,
            "status": self.status,
            "sort": self.sort,
            "open_type": self.open_type,
            "pid": self.pid,
        }

    def menu_json(self):
        type_map_dict = {"menu": 0, "path": 1}

        return {
            "id": self.id,
            "pid": self.pid,
            "title": self.name,
            "type": type_map_dict[self.type],
            "href": self.url,
            "icon": self.icon_sign,
            "sort": self.sort,
            "openType": self.open_type,
        }
