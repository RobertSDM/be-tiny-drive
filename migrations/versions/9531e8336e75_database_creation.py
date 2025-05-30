"""database_creation

Revision ID: 9531e8336e75
Revises: 
Create Date: 2025-05-26 11:34:39.787506

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9531e8336e75'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tb_account',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('creation_date', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tb_item',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('extension', sa.String(), nullable=False),
    sa.Column('size', sa.Integer(), nullable=False),
    sa.Column('size_prefix', sa.String(), nullable=False),
    sa.Column('type', sa.Enum('FILE', 'FOLDER', name='itemtype'), nullable=False),
    sa.Column('content_type', sa.String(), nullable=False),
    sa.Column('update_date', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('creation_date', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('parentid', sa.String(), nullable=True),
    sa.Column('ownerid', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['ownerid'], ['tb_account.id'], ),
    sa.ForeignKeyConstraint(['parentid'], ['tb_item.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tb_item')
    op.drop_table('tb_account')
    # ### end Alembic commands ###
