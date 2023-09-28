from pear_admin.extensions import db

from .department import DepartmentORM
from .rights import RightsORM
from .role import RoleORM
from .user import UserORM

user_role = db.Table(
    "ums_user_role",  # 用户-角色中间表名称
    db.Column("id", db.Integer, primary_key=True, autoincrement=True, comment="标识"),
    db.Column("user_id", db.Integer, db.ForeignKey("ums_user.id"), comment="用户编号"),
    db.Column("role_id", db.Integer, db.ForeignKey("ums_role.id"), comment="角色编号"),
)

role_rights = db.Table(
    "ums_role_rights",  # 用户-权限中间表名称
    db.Column("id", db.Integer, primary_key=True, autoincrement=True, comment="标识"),
    db.Column("rights_id", db.Integer, db.ForeignKey("ums_rights.id"), comment="用户编号"),
    db.Column("role_id", db.Integer, db.ForeignKey("ums_role.id"), comment="角色编号"),
)
