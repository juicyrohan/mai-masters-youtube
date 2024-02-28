Была выполнена предобработка комментариев:



Выделены признаки:
1. TF-IDf (TF-IDF)
2. Косинусная схожесть (Word2Vec)
3. Косинусная схожесть (FastText)
4. Токсичность по Достоевскому
5. Длина комментария
6. Количество эмодзи
7. Отношение знаков препинания

Была проведена стандартизация признаков (Standard Scaler).

Модели классификаторов:
1. Логистическая регрессия
2. Градиентный бустинг (LightGBM)
3. Наивный байесовский классификатор (Гауссовский)



Features:
1. TF-IDf
2. Cosine similarity (Word2Vec)
3. Cosine similarity (FastText)
4. Dostoevsky toxicity
5. Comment length
6. Number of emojis
7. Punctuation symbols ratio

Classifier models:
1. Logistic Regression
2. Gradient Boosting (LightGBM)
3. Gaussian Naive Bayes
