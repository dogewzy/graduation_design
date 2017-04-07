from model.db import Base, engine
Base.metadata.reflect(engine)  # 将数据映射绑定到引擎
Base.metadata.create_all(engine)