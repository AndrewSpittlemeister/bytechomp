from pathlib import Path
import sqlite3

from bytechomp import Reader, dataclass, Annotated
from bytechomp.datatypes import U8, U16, U32


@dataclass
class SQLiteHeader:
    header: Annotated[bytes, 16]
    page_size: U16
    file_format_write_version: U8
    file_format_read_version: U8
    reserved_space: U8
    max_embedded_payload_fraction: U8
    min_embedded_payload_fraction: U8
    leaf_payload_fraction: U8
    file_change_counter: U32
    number_of_pages: U32
    first_freelist_trunk_page: U32
    total_freelist_pages: U32
    schema_cookie: U32
    schema_format_number: U32
    default_page_cache_size: U32
    page_of_largest_root_btree: U32
    text_encoding: U32
    user_version: U32
    incremental_vacuum_mode: U32
    application_id: U32
    reserved: Annotated[list[U8], 20]
    version_valid_for: U32
    sqlite_version: U32


def create_sample_database(file: Path) -> None:
    conn = sqlite3.connect(str(file))

    # create table
    conn.execute(
        '''CREATE TABLE COMPANY(
            ID INT PRIMARY KEY     NOT NULL,
            NAME           TEXT    NOT NULL,
            AGE            INT     NOT NULL,
            ADDRESS        CHAR(50),
            SALARY         REAL
        );'''
    )

    # add some data
    conn.execute(
        "INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) VALUES (1, 'Paul', 32, 'California', 20000.00 )"
    )
    conn.execute(
        "INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) VALUES (2, 'Allen', 25, 'Texas', 15000.00 )"
    )
    conn.execute(
        "INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) VALUES (3, 'Teddy', 23, 'Norway', 20000.00 )"
    )
    conn.execute(
        "INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) VALUES (4, 'Mark', 25, 'Rich-Mond ', 65000.00 )"
    )
    conn.commit()

    # close connection
    conn.close()


def main() -> None:
    # find and clear database file
    sqlite_file = Path(__file__).parent.joinpath("test-db.sqlite").resolve()
    if sqlite_file.exists():
        sqlite_file.unlink()

    # create database file
    create_sample_database(sqlite_file)

    # create reader
    reader = Reader[SQLiteHeader]().allocate()

    # read from file until reader is satisfied
    with sqlite_file.open("rb") as fp:
        while not reader:
            reader << fp.read(1)

    # build header message
    print(reader.build())


if __name__ == "__main__":
    main()
