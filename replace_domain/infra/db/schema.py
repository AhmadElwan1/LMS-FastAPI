import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from replace_domain.infra.db.engine import metadata

authors = sa.Table(
    'authors',
    metadata,
    sa.Column('id', UUID(as_uuid=True), nullable=False, primary_key=True, server_default=sa.func.uuid_generate_v4()),
    sa.Column('name', sa.String(255), nullable=False),
    sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now()),
    sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
)

books = sa.Table(
    'books',
    metadata,
    sa.Column('id', UUID(as_uuid=True), nullable=False, primary_key=True, server_default=sa.func.uuid_generate_v4()),
    sa.Column('name', sa.String(255), nullable=False),
    sa.Column('description', sa.Text, nullable=True),
    sa.Column('number_of_pages', sa.Integer, nullable=False, default=1),
    sa.Column('is_borrowed', sa.Boolean, nullable=False, default=False),
    sa.Column('author_id', UUID(as_uuid=True), sa.ForeignKey('authors.id'), nullable=False),
    sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now()),
    sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
)
