# 代码生成模块

def init_app(app):
    from ruoyi_generator.controller.gen import gen
    app.register_blueprint(gen)