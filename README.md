Две версии файла:
1. main.py
2. app.py

Ситуация такая, вторая версия полностью чистая, готовая к использованию. Но. В ней отсутствует makeCarUrl так как он был перенесен непосредственно
в приложение чтобы оптимизировать тк сервер heroku не успепвал обрабатывать(некоторые ограничения бесплатной версии как я понял). Но остальные методы
+- доведены до ума.
Первая версия содержит в себе makeCarUrl, но за остальные методы не ручаюсь.

Необходимо объединить в одном файле две версии так чтобы был makeCarUrl из первой версии и остальные методы из второй.

P.S. Вторая версия содержит комменты.
