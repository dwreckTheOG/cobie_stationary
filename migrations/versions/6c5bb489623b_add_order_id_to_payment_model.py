"""Add order_id to Payment model

Revision ID: 6c5bb489623b
Revises: 75f174da8cf5
Create Date: 2024-10-15 00:07:04.540046

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6c5bb489623b'
down_revision = '75f174da8cf5'
branch_labels = None
depends_on = None


def upgrade():
    # Add the order_id column
    with op.batch_alter_table('payments', schema=None) as batch_op:
        batch_op.add_column(sa.Column('order_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(
            'fk_payments_order_id',  # Name of the foreign key constraint
            'orders',                # Referenced table
            ['order_id'],           # Local columns
            ['order_id'],           # Remote columns
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('payments', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.alter_column('sale_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.drop_column('order_id')

    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.alter_column('status',
               existing_type=sa.Enum('Pending', 'Sorting', 'Transporting', 'Completed', 'Cancelled'),
               type_=sa.VARCHAR(length=9),
               existing_nullable=True)

    # ### end Alembic commands ###
