from planner import db, login_manager
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000), nullable=False)
    amount = db.Column(db.String(100))
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.id"), nullable=False)

    def __repr__(self):
        return f"Ingredient('{self.name}', '{self.amount}')"


class Likes(db.Model):
    __tablename__ = "likes"
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.id"), primary_key=True)


class RecipeLabels(db.Model):
    __tablename__ = "recipe_labels"
    label_id = db.Column(db.Integer, db.ForeignKey("label.id"), primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.id"), primary_key=True)


class Label(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    recipes = db.relationship(
        "Recipe", secondary="recipe_labels", back_populates="labels"
    )

    def __repr__(self):
        return f"Label('{self.name}')"


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    time = db.Column(db.String(10))
    text = db.Column(db.String(2000), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    ingredients = db.relationship("Ingredient", backref="recipes", lazy=True)
    fans = db.relationship("User", secondary="likes", back_populates="favorite_recipes")
    labels = db.relationship(
        "Label", secondary="recipe_labels", back_populates="recipes"
    )

    def __repr__(self):
        return f"Recipe('title={self.title}', date_posted='{self.date_posted}', time='{self.time}, ingredients='{self.ingredients}, fans={self.fans}')"


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False)
    recipes = db.relationship("Recipe", backref="author", lazy=True)
    favorite_recipes = db.relationship(
        "Recipe", secondary="likes", back_populates="fans"
    )

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config["SECRET_KEY"], expires_sec)
        return s.dumps({"user_id": self.id}).decode("utf-8")

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            user_id = s.loads(token)["user_id"]
            return User.query.get(user_id)
        except Exception:
            return None

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
