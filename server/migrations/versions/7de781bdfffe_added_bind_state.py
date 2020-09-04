"""Added Bind State

Revision ID: 7de781bdfffe
Revises: e4b3d04da7fc
Create Date: 2020-09-04 21:47:57.400947

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = '7de781bdfffe'
down_revision = 'e4b3d04da7fc'
branch_labels = None
depends_on = None

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bind_state',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_on', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('updated_on', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('nameserver_1_ip', sqlalchemy_utils.types.ip_address.IPAddressType(length=255), nullable=False),
    sa.Column('nameserver_1_host', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('nameserver_1_host')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('bind_state')
    # ### end Alembic commands ###