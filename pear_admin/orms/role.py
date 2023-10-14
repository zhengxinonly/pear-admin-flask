from pear_admin.extensions import db

from ._base import BaseORM


class RoleORM(BaseORM):
    __tablename__ = "ums_role"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, comment="角色名称")
    code = db.Column(db.String(20), nullable=False, comment="角色标识符")
    desc = db.Column(db.Text)

    rights_ids = db.Column(
        db.String(512),
        comment="权限ids,1,2,5。冗余字段，用户缓存用户权限",
    )

    rights_list = db.relationship(
        "RightsORM", secondary="ums_role_rights", backref=db.backref("role")
    )

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "desc": self.desc,
            "rights_ids": self.rights_ids,
        }
