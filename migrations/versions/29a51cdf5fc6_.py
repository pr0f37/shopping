"""empty message

Revision ID: 29a51cdf5fc6
Revises: 
Create Date: 2020-10-04 21:57:13.597141

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "29a51cdf5fc6"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=20), nullable=False),
        sa.Column("email", sa.String(length=120), nullable=False),
        sa.Column("image_file", sa.String(length=20), nullable=False),
        sa.Column("password", sa.String(length=60), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("username"),
    )
    op.create_table(
        "recipe",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=100), nullable=False),
        sa.Column("date_posted", sa.DateTime(), nullable=False),
        sa.Column("time", sa.String(length=10), nullable=True),
        sa.Column("text", sa.String(length=2000), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"],),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "ingredient",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=10000), nullable=False),
        sa.Column("amount", sa.String(length=1000), nullable=True),
        sa.Column("recipe_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["recipe_id"], ["recipe.id"],),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "likes",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("recipe_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["recipe_id"], ["recipe.id"],),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"],),
        sa.PrimaryKeyConstraint("user_id", "recipe_id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("likes")
    op.drop_table("ingredient")
    op.drop_table("recipe")
    op.drop_table("user")
    # ### end Alembic commands ###
