# aimmo-refactoring

## 기술 스택
프레임워크 : python/flask
직렬화 : marshmallow
db : mongoengine, sqlite
문서화 도구 : flask-apispec

## 구현사항
1. 게시판 crud
2. 회원가입, 로그인
3. 게시글 카테고리
4. 게시글 검색
5. 대댓글(1depth)  
대댓글 pagination
6. 게시글 조회수  
같은 User가 게시글을 읽는 경우 count 수 증가하면 안 됨
   
7. unit test -- 진행중
8. 1000만건 이상의 데이터를 넣고 성능테스트 진행결과 -- 진행중


## 실행방법
다운로드 후
app.py와 같은 위치에 config.py를 만든후
```
SECRET_KEY = "비밀키"
JWT_SECRET_KEY = "비밀키"

SQLALCHEMY_TRACK_MODIFICATIONS = False

```
작성해주신 후에 아래와 같이하시면 됩니다.

```bash
#윈도우
python -m venv venv

source venv/Scripts/activate

pip install -r requirements.txt
```

```bash
#맥
python -m venv venv

source venv/bin/activate

pip install -r requirements.txt
```

```
flask run
```

## 구현방법 및 이유

1. RDB와 mongodb를 같이 쓴 이유  
회원같은 경우에는 mongodb보다 관계형 db로 관리하는 것이 우월하다고 판단하였습니다. 왜냐하면 회원정보는 글쓰는 것과 달리 변동가능성이 적고, 스키마 역시 확정적이기 때문입니다.
   이에 따라 회원정보는 rdb로 post정보는 mongodb로 관리하였습니다.
   
2. 댓글과 대댓글을 embedded로 구현한 이유.
 제가 고려한 선택지는 reference와 embedded였습니다. 그런데 일단 댓글, 대댓글, 게시글은 매우 밀접하게 관련이 있고, 댓글, 대댓글은 그 가벼움의 특성상 수정 가능성이 게시글보다 작다고 판단하였습니다.
   그리고 1000만건이 넘어가는 데이터가 저장되어있을시, 읽어올때의 속도를 고려하여 embedded로 구현하였습니다.
   