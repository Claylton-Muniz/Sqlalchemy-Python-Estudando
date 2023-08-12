from sqlalchemy import create_engine, inspect, select
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, Session

Base = declarative_base()


class User(Base):
    __tablename__ = "user_account"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)

    address = relationship("Address", back_populates="user", cascade="all, delete-orphan")


    def __repr__(self):
        return f"user (id={self.id}, name={self.name}, fullname={self.fullname})"


class Address(Base):
    __tablename__ = "address"

    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("user_account.id"), nullable=False)

    user = relationship("User", back_populates="address")


    def __repr__(self):
        return f"address (id={self.id}, email_address={self.email_address})"


engine = create_engine("sqlite://")
Base.metadata.create_all(engine)

insp_engine = inspect(engine)

print(insp_engine.get_table_names())

with Session(engine) as session:
    claylton = User(
        name="Claylton",
        fullname="Claylton Muniz",
        address=[Address(email_address="claymuniz67@gmail.com"),
                Address(email_address="tetsunogamer@gmail.com")]
    )

    test = User(
        name="Test",
        fullname="The Test",
        address=[Address(email_address="test@gmail.com")]
    )

    test2 = User(
        name="Test2",
        fullname="The Test2"
    )

    session.add_all([claylton, test, test2])
    session.commit()

stmt = select(User, Address).join_from(User, Address)

connection = engine.connect()
results = connection.execute(stmt)

for result in results:
    print(result)
