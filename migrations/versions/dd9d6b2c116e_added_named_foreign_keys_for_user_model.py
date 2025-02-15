"""Added named foreign keys for User model

Revision ID: dd9d6b2c116e
Revises: 410efff0d6a3
Create Date: 2025-02-15 17:13:21.989721

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dd9d6b2c116e'
down_revision = '410efff0d6a3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('faculty_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('department_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_user_department', 'departments', ['department_id'], ['id'])
        batch_op.create_foreign_key('fk_user_faculty', 'faculties', ['faculty_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint('fk_user_faculty', type_='foreignkey')
        batch_op.drop_constraint('fk_user_department', type_='foreignkey')
        batch_op.drop_column('department_id')
        batch_op.drop_column('faculty_id')

    # ### end Alembic commands ###
