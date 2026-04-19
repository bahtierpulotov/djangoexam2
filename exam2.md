

## Кори имтиҳонӣ аз Django (MVT)

### Мавзӯи лоиҳа

**Мини-китобхона / Book Catalog**

---

## Ҳадафи кор

Сохтани як лоиҳаи пурраи Django MVT, ки дар он донишҷӯ нишон диҳад, ки метавонад:

* бо архитектураи Django MVT кор кунад
* моделҳо ва алоқаҳои байни ҷадвалҳоро созад
* саҳифаҳо бо template эҷод кунад
* CRUD-ро бо Function-Based Views (FBV) иҷро кунад
* QuerySet ва ҷустуҷӯро истифода барад
* бақайдгирӣ ва воридшавиро (authentication) амалӣ созад
* тасдиқи email, reset password ва change password-ро иҷро кунад

---

## Тавсифи умумии лоиҳа

Сохтани сайт бо номи **«Мини-китобхона»**, ки корбар метавонад:

* рӯйхати китобҳоро бинад
* китобҳоро ҷустуҷӯ кунад
* китобҳоро филтр кунад
* саҳифаи муфассали китобро кушояд
* китоб илова, таҳрир ва нест кунад
* сабти ном кунад, ворид шавад ва барояд
* email-ро тасдиқ кунад
* паролро иваз ва барқарор кунад

---

## Талаботи техникӣ

### 1. Сохтори лоиҳа

Донишҷӯ бояд эҷод кунад:

* 1 Django project
* камаш 1 app

Лоиҳа бояд бе хатогӣ кор кунад.

---

### 2. Моделҳо

Дар лоиҳа бояд ин моделҳо бошанд:

#### 1) Category (Категория)

Майдонҳо:

* name (ном)

#### 2) Author (Муаллиф)

Майдонҳо:

* full_name (номи пурра)
* bio (маълумот дар бораи муаллиф)

#### 3) Book (Китоб)

Майдонҳо:

* title (ном)
* description (тавсиф)
* price (нарх)
* cover_image (расми муқова)
* created_at (санаи эҷод)
* author → ForeignKey
* category → ForeignKey
* created_by → ForeignKey ба User

#### 4) Review (Барраси / Шарҳ)

Майдонҳо:

* book → ForeignKey
* user → ForeignKey ба User
* text (матн)
* rating (баҳо)
* created_at (сана)

---

### 3. Алоқа байни моделҳо

Бояд нишон дода шавад:

* Book → Author : ForeignKey
* Book → Category : ForeignKey
* Review → Book : ForeignKey
* Review → User : ForeignKey

Инчунин бояд reverse relation фаҳмида шавад:

* аз китоб → ҳамаи review-ҳо
* аз author → ҳамаи китобҳояш

---

### 4. Migrations

Донишҷӯ бояд:

* моделҳо созад
* `makemigrations` иҷро кунад
* `migrate` иҷро кунад

---

### 5. Admin panel

Дар Django admin бояд CRUD кор кунад барои:

* Category
* Author
* Book
* Review

---

### 6. Templates

Бояд ин template-ҳо бошанд:

* base.html
* home page
* book_list.html
* book_detail.html
* book_create.html
* book_update.html
* book_delete.html
* register.html
* login.html
* profile.html

**Талабот:**

* истифодаи template inheritance
* гузаронидани маълумот аз view ба template
* истифодаи template tags ва filters
* пайваст кардани static files
* танзими media files

---

### 7. CRUD бо FBV

Барои модели Book бояд CRUD пурра сохта шавад:

* Create (эҷод)
* Read (хондан)
* Update (тағйир додан)
* Delete (нест кардан)

Бояд истифода шавад:

* render
* redirect
* get_object_or_404
* кор бо GET ва POST

---

### 8. QuerySet, filter ва search

Дар саҳифаи рӯйхати китобҳо:

* нишон додани ҳамаи китобҳо
* ҷустуҷӯ бо номи китоб
* филтр бо категория
* филтр бо муаллиф
* истифодаи exclude()
* гирифтани як объект бо get() ё get_object_or_404()

Методҳои ORM:

* all()
* get()
* filter()
* exclude()

Lookup fields:

* title__icontains
* price__gte
* price__lte

---

### 9. Reverse relation

Дар саҳифаи тафсилоти китоб:

* маълумоти китоб
* ҳамаи review-ҳо
* номи муаллиф
* категория

---

### 10. select_related ва prefetch_related

Оптимизатсияи query:

* дар list → select_related() барои author ва category
* дар detail → prefetch_related() барои review

---

### 11. Aggregate ва annotate

Сохтани саҳифаи **Статистика**

* шумораи умумии китобҳо
* нархи миёна
* баҳои миёна
* шумораи китобҳо барои ҳар муаллиф

Методҳо:

* aggregate()
* annotate()

---

### 12. Authentication

Бояд бошад:

* Register
* Login
* Logout

Қоидаҳо:

* танҳо user-и сабтшуда метавонад китоб илова кунад
* танҳо муаллифи китоб ё admin метавонад edit/delete кунад
* user-и ношинос танҳо мебинад

---

### 13. Тасдиқи Email

Баъд аз бақайдгирӣ user бояд email-ро тасдиқ кунад.

Метавон истифода бурд:

* console backend
* Mailtrap
* дигар test email

Муҳим — нишон додани логика.

---

### 14. Парол

Бояд бошад:

* Reset password
* Change password

---

### 15. Дизайн

* саҳифаҳо тоза ва фаҳмо бошанд
* navigation осон бошад
* код хондашаванда бошад
* номгузорӣ дуруст бошад

---

### 16. Чӣ бояд супорида шавад

* папкаи лоиҳа
* requirements.txt
* README.md (чӣ гуна запуск кардан, саҳифаҳо, функсияҳо)
* скриншотҳо
* базаи SQLite (метавонад дар проект бошад)

---

### 17. Дар ҳимоя (защита)

Донишҷӯ бояд фаҳмонад:

* Django чист
* фарқи MVT ва MVC
* request чӣ гуна меояд
* view чӣ гуна кор мекунад
* template чӣ гуна маълумот мегирад
* моделҳо ва migration чӣ гунаанд
* CRUD чӣ гуна аст
* QuerySet ва filter чӣ гуна кор мекунанд
* authentication чӣ гуна аст
* select_related, prefetch_related, aggregate, annotate барои чӣ лозиманд

---

## Хулоса (супориши кӯтоҳ)

Сохтани Django-проект **«Мини-китобхона»**, ки дорои:

* китобҳо
* муаллифон
* категорияҳо
* review

Ва амалӣ кардани:

* моделҳо
* template
* CRUD (бо FBV)
* ҷустуҷӯ ва филтр
* authentication
* email confirmation
* reset/change password
* QuerySet, reverse relation
* select_related, prefetch_related
* aggregate ва annotate

---
