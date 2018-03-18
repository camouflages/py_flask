from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from zhihu import app
from exts import db

manager=Manager()

#使用migrate 绑定app和db
migrate=Migrate()

#添加迁移脚本命令道manager中

manager.add_command('db',MigrateCommand)

if __name__=='__main__':
    manager.run()