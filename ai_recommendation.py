def generate_ai_recommendation(
    skin_type,
    problem,
    best_product
):

    if skin_type == "Berminyak" and problem == "Jerawat":
        return f"""
AI merekomendasikan {best_product}
karena kandungannya membantu mengontrol
minyak berlebih dan mengurangi jerawat.
"""

    elif skin_type == "Kering":
        return f"""
AI merekomendasikan {best_product}
karena membantu menjaga kelembaban kulit
dan memperkuat skin barrier.
"""

    elif skin_type == "Sensitif":
        return f"""
AI merekomendasikan {best_product}
karena formulanya lebih lembut untuk kulit sensitif.
"""

    return f"""
AI merekomendasikan {best_product}
berdasarkan hasil analisis graph dan Dijkstra.
"""