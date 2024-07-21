from flask import Blueprint, jsonify, request
from flask_login import login_required
from classes.salesAnalysis import vendaAnalise
from datetime import datetime
import logging
from database.mongodb import db
from decorators import admin_required

vendas_bp = Blueprint('vendas', __name__)

logging.basicConfig(level=logging.INFO)

@vendas_bp.route('/salesAnalysis', methods=['GET'])
@login_required
@admin_required
def analiseVenda():
    try:
        start_date_str = request.args.get('data_inicio')
        end_date_str = request.args.get('data_fim')
        
        if not start_date_str or not end_date_str:
            logging.error("Parâmetros data_inicio e data_fim são obrigatórios")
            return jsonify({"error": "Parâmetros data_inicio e data_fim são obrigatórios"}), 400
        
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        
        end_date = end_date.replace(hour=23, minute=59, second=59, microsecond=999999)

        logging.info(f"Consultando vendas de {start_date} até {end_date}")

        totalSales = vendaAnalise.getSales(start_date, end_date)
        averageSales = vendaAnalise.getMediaSales(start_date, end_date)
        salesCount = vendaAnalise.getSalesCount(start_date, end_date)
        sales = vendaAnalise.getSalesData(start_date, end_date)

        logging.info(f"Resultados da análise: totalSales={totalSales}, averageSales={averageSales}, salesCount={salesCount}")

        analysisResult = {
            "totalSales": totalSales,
            "averageSales": averageSales,
            "salesCount": salesCount,
            "sales": sales
        }

        return jsonify(analysisResult), 200

    except Exception as e:
        logging.error(f"Erro ao realizar análise de vendas: {e}")
        return jsonify({"error": "Erro ao realizar análise de vendas"}), 500
