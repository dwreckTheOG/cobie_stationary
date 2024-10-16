"""image

Revision ID: 75f174da8cf5
Revises: a3997745c463
Create Date: 2024-10-14 14:34:25.293158

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '75f174da8cf5'
down_revision = 'a3997745c463'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('carts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('status', sa.Enum('pending', 'ordered', name='cartstatus'), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('carts', schema=None) as batch_op:
        batch_op.drop_column('status')

    # ### end Alembic commands ###
