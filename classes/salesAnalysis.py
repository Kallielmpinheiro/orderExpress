from database.mongodb import db

class vendaAnalise:

    @staticmethod
    def getSales(start_date, end_date):
        pedidos = db.pedidos
        total_sales = pedidos.aggregate([
            {
                "$match": {
                    "status": "pago",
                    "created_at": {"$gte": start_date, "$lte": end_date}
                }
            },
            {
                "$group": {
                    "_id": None,
                    "total": {"$sum": "$total_price"}
                }
            }
        ])
        result = list(total_sales)
        if result:
            return result[0]['total']
        else:
            return 0

    @staticmethod
    def getMediaSales(start_date, end_date):
        pedidos = db.pedidos
        media_sales = pedidos.aggregate([
            {
                "$match": {
                    "status": "pago",
                    "created_at": {"$gte": start_date, "$lte": end_date}
                }
            },
            {
                "$group": {
                    "_id": None,
                    "average": {"$avg": "$total_price"}
                }
            }
        ])
        result = list(media_sales)
        if result:
            return result[0]['average']
        else:
            return 0

    @staticmethod
    def getSalesCount(start_date, end_date):
        pedidos = db.pedidos
        sales_count = pedidos.count_documents({
            "status": "pago",
            "created_at": {"$gte": start_date, "$lte": end_date}
        })
        return sales_count
    
    @staticmethod
    def getSalesData(start_date, end_date):
        pedidos = db.pedidos
        sales_data = pedidos.find({
            "status": "pago",
            "created_at": {"$gte": start_date, "$lte": end_date}
        }, {"created_at": 1, "total_price": 1}).sort("created_at", 1)
        
        sales = [{"date": sale["created_at"].strftime('%Y-%m-%d'), "amount": sale["total_price"]} for sale in sales_data]
        return sales
