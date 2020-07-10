# DB Specification
## Company
|<center>Column</center>|<center>Type</center>|<center>Key</center>|<center>Description</center>|
|----|------|--|--|
`company_id`| VARCHAR(255)|<center>Primary</center>|Company를 구분짓는 unique한 ID
## Language
|<center>Column</center>|<center>Type</center>|<center>Key</center>|<center>Description</center>|
|----|------|--|--|
`language_id`| VARCHAR(5)|<center>Primary</center>|Language를 구분짓는 unique한 ID
## CompanyInfo
|<center>Column</center>|<center>Type</center>|<center>Key</center>|<center>Description</center>|
|----|------|--|--|
`company_id`| VARCHAR(255)|<center>Primary<br>Company.company_id</center>|Company를 구분짓는 unique한 ID
`language_id`| VARCHAR(5)|<center>Foreign<br>Language.language_id</center>|Language를 구분짓는 unique한 ID
`name`| VARCHAR(255)||회사 이름
`tag`| VARCHAR(255)||회사 태그
<br>

# API Specification
## 1. Company
### `/company/register/<company_id>`
|    |      |
|----|------|
기능 |하나의 `Company` 등록한다.
Method|POST
URL Params|`company_id<string>`: 생성하고자 하는 `Company`의 ID.

#### Success Response
http://127.0.0.1:5000/company/register/id_new_company
|    |      |
|----|------|
Code`<int>`| 201
Response`<json>`|
```json
{
  "message": "Successfully registered.",
  "status": "success"
}
```
#### Fail Response
http://127.0.0.1:5000/company/register/id_new_company
|    |      |
|----|------|
Code`<int>`| 200
Response`<json>`|
```json
{
  "message": "Company already exists.",
  "status": "fail"
}
```

### `/company/<company_id>`
|    |      |
|----|------|
기능 |ID로 회사를 검색한다.
Method|GET
URL Params|`company_id<string>`: 검색하고자 하는 `Company`의 ID.

#### Success 
http://127.0.0.1:5000/company/id_new_company
|    |      |
|----|------|
Code`<int>`| 200
Response`<json>`|
```json
{
  "company_id": "id_new_company"
}
```
#### Fail
|    |      |
|----|------|
Code`<int>`| 204: ID에 해당하는 `Company`가 없을때 
Response| No Content

### `/company/delete/<string:company_id>`
|    |      |
|----|------|
기능 |하나의 `Company`를 삭제한다.
Method|POST
URL Params|`company_id<string>`: 삭제하고자 하는 `Company`의 ID.

#### Success 
http://127.0.0.1:5000/company/delete/id_duplicated
|    |      |
|----|------|
Code`<int>`| 200
Response`<json>`|
```json
{
  "message": "Successfully deleted.",
  "status": "success"
}
```
#### Fail
http://127.0.0.1:5000/company/delete/id_not_existed
|    |      |
|----|------|
Code`<int>`| 200
Response`<json>`|
```json
{
  "message": "There is no the Company by id(id_not_existed).",
  "status": "fail"
}
```

## 2. Language
### `/language/register/<string:language_id>`
|    |      |
|----|------|
기능 |하나의 `Language` 등록한다.
Method|POST
URL Params|`language_id<string>`: 등록하고자 하는 `Language` ID.

#### Success 
http://127.0.0.1:5000/language/register/id_new_language
|    |      |
|----|------|
Code`<int>`| 201
Response`<json>`|
```json
{
  "message": "Successfully registered.",
  "status": "success"
}
```
#### Fail
http://127.0.0.1:5000/company/delete/id_duplicated_language
|    |      |
|----|------|
Code`<int>`| 200
Response`<json>`|
```json
{
  "message": "The language(id_duplicated_language) already exists.",
  "status": "fail"
}
```

### `/languages`
|    |      |
|----|------|
기능 |등록된 `Language` 전부를 검색한다.
Method|GET

#### Success 
http://127.0.0.1:5000/languages
|    |      |
|----|------|
Code`<int>`| 200
Reponse`<json>`| 
```json
{
  "languages": [
    "ko",
    "en",
    "ja",
    "ch"
  ]
}
```
#### Fail
|    |      |
|----|------|
Code`<int>`| 204: 등록된 `Language`가 아무것도 없을때 
Response| No Content

### `/language/delete/<string:language_id>`
|    |      |
|----|------|
기능 |하나의 `Language` 삭제한다.<br>단, `DEFAULT_LOCALE`로 사용중인 값은 삭제 할 수 없다,
Method|POST
URL Params|`language_id<string>`: 삭제하고자 하는 `Language` ID.

#### Success 
http://127.0.0.1:5000/language/register/id_exist_language
|    |      |
|----|------|
Code`<int>`| 200
Response`<json>`| 
```json
{
  "message": "Successfully deleted.",
  "status": "success"
}
```
#### Fail
http://127.0.0.1:5000/language/delete/id_default_locale
|    |      |
|----|------|
Code`<int>`| 423: 삭제하려는 `Language`가 `DEFAULT_LOCALE`로 설정된 값고 같을 때 
Response`<json>`| 
```json
{
  "message": "The language_id(id_default_locale) is default locale.",
  "status": "fail"
}
```
http://127.0.0.1:5000/language/delete/id_not_exist
|    |      |
|----|------|
Code`<int>`| 200
Response`<json>`| 
```json
{
  "message": "There is no language by id(id_not_exist)",
  "status": "fail"
}
```

### `/locale/<string:language_id>`
|    |      |
|----|------|
기능 |등록된 하나의 `Language`를 `DEFAULT_LOCALE`로 설정한다.<br>다수의 언어 데이터가 있다면, `DEFAULT_LOCALE`로 설정된 언어로 매핑된 데이터를 기본으로 전송한다.<br>예를 들어, 태그로 검색한 결과가 여러개의 언어로 존재한다면, 해당 설정값과 일치하는 언어 데이터를 전달한다.
Method|POST
URL Params|`language_id<string>`: 설정하고자 하는 `Language` ID.

#### Success 
http://127.0.0.1:5000/locale/en
|    |      |
|----|------|
Code`<int>`| 200
Response`<json>`| 
```json
{
  "message": "Successfully changed `DEFAULT_LOCALE` to en.",
  "status": "success"
}
```
http://127.0.0.1:5000/company/tag/태그_4

```json
{
...,
  "86": {
    "company_id": "86",
    "display_name": "OKAY.com",
    "language_id": "ko",
    "name": null,
    "tag": "태그_24|태그_27|태그_4"
  },
  "90": {
    "company_id": "90",
    "display_name": "Rejoice Pregnancy",
    "language_id": "ko",
    "name": null,
    "tag": "태그_22|태그_30|태그_7|태그_4"
  },
  "id_wanted": {
    "company_id": "id_wanted",
    "display_name": "Wantedlab",
    "language_id": "ko",
    "name": "원티드랩",
    "tag": "태그_4|태그_20|태그_16"
  }
}
```

## 3. CompanyInfo
### `/company/<string:company_id>/register`
|    |      |
|----|------|
기능  |하나의 `CompanyInfo` 전체 데이터를 등록한다.
Method|POST
URL Params|`company_id<string>`: 등록할 정보의 `Company` ID
Data Params|`name<string>`: Company name<br>`tag<string>`: Global delimiter로 연결되어 있는 하나의 tag 또는 다수의 tags<br>`language_id<string>`: 등록할 `CompanyInfo`의 언어 정보.

#### Success 
http://127.0.0.1:5000/company/id_company/register
|    |      |
|----|------|
Code`<int>`| 201
Content`<json>`| 
```json
{
    "name": "ja_company",
    "tag": "tag_x|tag_y|tag_z",
    "language_id": "ja"
}
```
Response`<json>`
```json
{
  "message": "Successfully registered.",
  "status": "success"
}
```
#### Fail
http://127.0.0.1:5000/company/34/register
|    |      |
|----|------|
Code`<int>`| 200
Content`<json>`| 
```json
{
  "message": "Already exist company information by parameters(company_id(34), language_id(ja)).",
  "status": "fail"
}
```
### `/company/<string:company_id>/info`
|    |      |
|----|------|
기능  |ID로 회사 정보를 검색한다.
Method|GET
URL Params|company_id`<string>`: `Company` ID

#### Success 
http://127.0.0.1:5000/company/id_wanted/info
|    |      |
|----|------|
Code`<int>`| 200
Content`<json>`| 
```json
[
  {
    "company_id": "id_wanted",
    "language_id": "en",
    "name": "Wantedlab",
    "tag": "tag_4|tag_20|tag_16"
  },
  {
    "company_id": "id_wanted",
    "language_id": "ja",
    "name": null,
    "tag": "タグ_4|タグ_20|タグ_16"
  },
  {
    "company_id": "id_wanted",
    "language_id": "ko",
    "name": "원티드랩",
    "tag": "태그_4|태그_20|태그_16"
  }
]
```
#### Fail
http://127.0.0.1:5000/company/id_wanted/info
|    |      |
|----|------|
Code`<int>`| 204: 입력받은 ID와 일치하는 정보가 없을 때
Content`<json>`| No Content

### `/company/name/<string:name>`
|    |      |
|----|------|
기능  |이름으로 회사 정보를 검색한다.
Method|GET
URL Params|name`<string>`: `Company` 이름의 일부분

#### Success 
http://127.0.0.1:5000/company/name/want
|    |      |
|----|------|
Code`<int>`| 200
Content`<json>`| 
```json
{
  "id_wanted": {
    "company_id": "id_wanted",
    "language_id": "ko",
    "name": "원티드랩",
    "tag": "태그_4|태그_20|태그_16"
  }
}
```
#### Fail
http://127.0.0.1:5000/company/name/not_exist_name
|    |      |
|----|------|
Code`<int>`| 204: 입력받은 이름과 일치하는 정보가 없을 때
Content`<json>`| No Content

### `/company/<string:company_id>/register/tag`
|    |      |
|----|------|
기능  | 하나 또는 다수의 태그를 추가한다.
Method|POST
URL Params|`company_id<string>`: 태그를 등록 할 회사의 ID
Data Params|`languages<list>`: 태그를 등록 할 언어 정보<br>`tag<list>`: 등록 할 태그 목록

#### Success 
http://127.0.0.1:5000/company/id_wanted/register/tag
|    |      |
|----|------|
Code`<int>`| 200
Content`<json>`| 
```json
{
    "languages": ["ko", "en"],
    "tag": ["hello", "world"]
}
```
Response`<json>`
```json
{
  "message": "Successfully registered.",
  "status": "success"
}
```

#### Fail
http://127.0.0.1:5000/company/id_not_exist/register/tag
|    |      |
|----|------|
Code`<int>`| 200
Content`<json>`|
```json
{
  "message": "There is no company by company_id(id_not_exist)",
  "status": "fail"
}
```
### `/company/tag/<string:tags>`
|    |      |
|----|------|
기능  | 하나 또는 다수의 태그로 회사 정보를 검색한다.
Method|GET
URL Params|tag`<string>`: 회사정보에 포함된 태그, 다수의 값일 경우 `DELIMITER`로 연결된 문자열.

#### Success 
http://127.0.0.1:5000/company/tag/tag_4
|    |      |
|----|------|
Code`<int>`| 200
Content`<json>`| 

```json
{
  "34": {
    "company_id": "34",
    "display_name": "보비어스코리아",
    "language_id": "en",
    "name": null,
    "tag": "tag_11|tag_8|tag_3|tag_4"
  },
  ...,
  "90": {
    "company_id": "90",
    "display_name": null,
    "language_id": "en",
    "name": "Rejoice Pregnancy",
    "tag": "tag_22|tag_30|tag_7|tag_4"
  },
  "id_wanted": {
    "company_id": "id_wanted",
    "display_name": "원티드랩",
    "language_id": "en",
    "name": "Wantedlab",
    "tag": "tag_4|tag_20|tag_16"
  }
}
```
http://127.0.0.1:5000/company/tag/tag_1|tag_5
```json
{
  "15": {
    "company_id": "15",
    "display_name": "YG PLUS",
    "language_id": "en",
    "name": null,
    "tag": "tag_1|tag_16|tag_5"
  },
...,
  "72": {
    "company_id": "72",
    "display_name": "쿠차",
    "language_id": "en",
    "name": null,
    "tag": "tag_27|tag_5|tag_26"
  },
  "77": {
    "company_id": "77",
    "display_name": "티엠씨케이",
    "language_id": "en",
    "name": null,
    "tag": "tag_1|tag_26|tag_19|tag_17"
  },
  "96": {
    "company_id": "96",
    "display_name": null,
    "language_id": "en",
    "name": "Grab",
    "tag": "tag_1"
  }
}
```
#### Fail
http://127.0.0.1:5000/company/tag/not_exist
|    |      |
|----|------|
Code`<int>`| 204: 입력받은 태그와 일치하는 정보가 없을 때
Content`<json>`| No Content

### `/company/<string:company_id>/delete/tag`
|    |      |
|----|------|
기능  | 하나 또는 다수의 태그를 삭제한다.
Method|POST
URL Params|`company_id<string>`: 삭제할 태그가 포함된 회사의 ID
Data Params|`languages<list>`: 태그를 삭제 할 언어 정보<br>`tag<list>`: 삭제 할 태그 목록

#### Success 
http://127.0.0.1:5000/company/id_wanted/delete/tag
|    |      |
|----|------|
Code`<int>`| 200
Content`<json>`| 
```json
{
    "languages": ["ko", "en"],
    "tag": ["tag_tt", "tag_qq"]
}
```
Response`<json>`
```json
{
  "message": "Successfully deleted.",
  "status": "success"
}
```

#### Fail
http://127.0.0.1:5000/company/id_not_exist/delete/tag
|    |      |
|----|------|
Code`<int>`| 200
Content`<json>`|
```json
{
  "message": "There is no company by company_id(id_not_exist)",
  "status": "fail"
}
```