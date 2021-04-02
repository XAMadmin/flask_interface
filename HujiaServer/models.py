from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.orm import Session

metadata = MetaData()
engine = create_engine(
      "",  # 数据库配置
      echo = False
)



# 客户token表
Customer = Table('customer_token', metadata, autoload=True, autoload_with=engine)


# 40货位商品库存
Order = Table('sphwph_40', metadata, autoload=True, autoload_with=engine)


# 商品信息
Spkfk = Table('spkfk', metadata, autoload=True, autoload_with=engine)


# hj_spptkcdj华嘉商品提交
HjOrder = Table('hj_spptkcdj', metadata, autoload=True, autoload_with=engine)


# 出库信息
OrderOutStore = Table('spls_hz', metadata, autoload=True, autoload_with=engine)

session = Session(engine)

data = session.query(Customer).filter_by(dwbh = 'DWI000002991').first()
print(data)