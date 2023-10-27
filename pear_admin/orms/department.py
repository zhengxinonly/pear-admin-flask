from pear_admin.extensions import db

from ._base import BaseORM


class DepartmentORM(BaseORM):
    __tablename__ = "ums_department"
    id = db.Column(db.Integer, primary_key=True, comment="部门ID")
    name = db.Column(db.String(50), comment="部门名称")
    leader = db.Column(db.String(50), comment="负责人")
    enable = db.Column(db.Boolean, comment="状态(1开启,0关闭)", default=True)

    users = db.relationship("UserORM", backref="department")

    pid = db.Column(db.Integer, db.ForeignKey("ums_department.id"), default=1)
    parent = db.relationship(
        "DepartmentORM", back_populates="children", remote_side=[id]
    )  # 自关联
    children = db.relationship("DepartmentORM", back_populates="parent")

    def json(self):
        return {
            "id": self.id,
            "pid": self.pid,
            "name": self.name,
            "leader": self.leader,
            "enable": self.enable,
        }
