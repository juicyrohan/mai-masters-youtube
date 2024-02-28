Цель исследования - разработка алгоритма классификации комментариев для обнаружения ботов и троллей в комментариях на площадке YouTube.

На первом этапе рассматриваем два класса:
  1. Обычные комментарии
  2. Комментарии ботов и троллей

В дальнейшем будем рассматривать ботов и троллей как отдельные классы.

Была выполнена предобработка комментариев:



Выделены **признаки**:
  1. TF-IDF
  2. Косинусное сходство (Word2Vec)
  3. Косинусная сходство (FastText)
  4. Токсичность комментария (Dostoevsky)
  5. Длина комментария
  6. Количество эмодзи
  7. Доля знаков препинания в общем кол-ве символов

Была проведена **стандартизация** всех признаков (Standard Scaler).

Также в силу дисбаланса классов был применен метод **пересемплирования** SMOTE.<br>
!!! Добавить другие методы пересемплирования: ADASYN, Random OverSampler ...

Модели **классификаторов**:
  1. Логистическая регрессия
  2. Градиентный бустинг (LightGBM)
  3. Наивный байесовский классификатор (Гауссовский)

Было проведено сравнение качества моделей по различным наборам признаков. Лучшие результаты для каждой модели:

  1. Logistic Regression<br>
  **Best Metrics** by auc_roc:<br>
    accuracy: 0.57<br>
    precision: 0.54 <br>
    recall: 0.74 <br>
    f1: 0.63 <br>
    auc_roc: 0.58<br>
  **Best Features**: wv, comment_length, emoji_count, punct<br>
  
  3. Gaussian Naive Bayes<br>
  **Best Metrics** by auc_roc:<br>
    accuracy: 0.58 <br>
    precision: 0.54 <br>
    recall: 0.91 <br>
    f1: 0.68 <br>
    auc_roc: 0.59<br>
  **Best Features**: ft, tfidf, comment_length, emoji_count, punct<br>
  
  5. LigthGBM<br>
  **Best Metrics** by auc_roc:<br>
    accuracy: 0.96 <br>
    precision: 0.95 <br>
    recall': 0.98 <br>
    f1: 0.96 <br>
    auc_roc: 0.97<br>
  **Best Features**: wv, ft, tfidf, comment_length, emoji_count, punct<br>
  
!!! Здесь можно проверить гипотезу о равенстве auc roc для разных наборов признаков (есть ли статистически значимое различие).


<!--
Features:
1. TF-IDF
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
-->
