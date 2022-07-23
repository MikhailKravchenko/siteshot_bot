create table users
(
    user_id    int not null
        constraint user_pk
            primary key,
    user_name  varchar(100),
    first_name varchar(100),
    created_at timestamp default now(),
    update_at  timestamp default now()
);

create table request
(
    request_id serial
        constraint request_pk
            primary key,
    url        text,
    domen      text,
    success    boolean,
    user_id    integer
        constraint request_user_user_id_fk
            references users
            on update cascade on delete cascade,
    file_name  varchar(50),
    file_path  varchar(250),
    duration   integer,
    created_at timestamp default now()
);

alter table request
    owner to sib5;

create unique index request_request_id_uindex
    on request (request_id);



create unique index request_request_id_uindex
    on request (request_id);

