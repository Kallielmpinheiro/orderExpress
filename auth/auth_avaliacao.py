import logging
from flask import Blueprint, request, redirect, url_for, flash, render_template
from flask_login import login_required, current_user
from bson import ObjectId
from database.mongodb import db
from classes.user import User

logging.basicConfig(level=logging.DEBUG)

avaliacao_bp = Blueprint('avaliacao', __name__)

@avaliacao_bp.route('/avaliar/<product_id>', methods=['POST'])
@login_required
def avaliar_produto(product_id):
    try:
        rating = int(request.form['estrelas_user'])
        comment = request.form['comentario_user']
        user_cpf = current_user.cpf

        user = User.getUserByCpf(user_cpf)
        if not user:
            logging.error(f"Usuário com CPF {user_cpf} não encontrado")
            flash('Usuário não encontrado.')
            return redirect(url_for('user.index'))

        logging.debug(f"Dados do usuário recuperados: {user.dict()}")

        product = db.products.find_one({"_id": ObjectId(product_id)})
        if not product:
            logging.error(f"Produto com ID {product_id} não encontrado")
            return redirect(url_for('user.index'))

        review = {
            "product_id": ObjectId(product_id),
            "user_cpf": user.cpf,
            "username": user.nomeCompleto,
            "rating": rating,
            "comment": comment
        }

        existing_review = db.reviews.find_one({"product_id": ObjectId(product_id), "user_cpf": user.cpf})
        if existing_review:
            logging.error(f"Usuário {user.cpf} já avaliou o produto {product_id}")
            flash('Você já avaliou este produto.')
            return redirect(url_for('user.index'))

        db.reviews.insert_one(review)
        logging.debug(f"Avaliação salva: {review}")

        all_reviews = list(db.reviews.find({"product_id": ObjectId(product_id)}))
        total_reviews = len(all_reviews)
        average_rating = sum([r['rating'] for r in all_reviews]) / total_reviews

        db.products.update_one(
            {"_id": ObjectId(product_id)},
            {
                "$set": {
                    "quantidade_avaliacoes": total_reviews,
                    "media_estrelas": average_rating
                }
            }
        )

        logging.info(f"Avaliação adicionada para o produto {product_id} por {user.cpf}")
        flash('Avaliação enviada com sucesso!')
        return redirect(url_for('user.index'))

    except Exception as e:
        logging.error(f"Erro ao avaliar o produto: {e}")
        flash('Erro ao enviar a avaliação.')
        return redirect(url_for('user.index'))