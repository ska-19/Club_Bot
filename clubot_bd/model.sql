create schema if not exists clubot_bd;
set search_path = clubot_bd, public;

drop table if exists users cascade;
create table users (
    id serial primary key,
    username varchar(255) not null, -- tg handler
    mentor bool not null, -- default false
    email varchar(255),
    password varchar(255) not null, -- tg_id
    name varchar(255) not null, -- tg name
    surname varchar(255) not null, -- tg surname
    dob date,
    tel varchar(255),
    date_joined date not null,
    photo text, --link
    comfort_time text, -- meeting time
    course varchar(255),
    faculty varchar(255),
    links text, -- links to social media
    bio text
);

drop table if exists club cascade;
create table club (
    id serial primary key,
    owner integer not null,
    name varchar(255) not null,
    dest text,
    photo text, --link
    bio text,
    links text, --links to social media
    date_created date,
    date_joined date not null,
    comfort_time text, -- meeting time
    --todo add очивки, валюта, призы и тд
    foreign key (owner) references users(id)
);

drop table if exists club_x_user cascade;
create table club_x_user (
    id serial primary key,
    club_id integer not null,
    user_id integer not null,
    role varchar(255) not null,
    date_joined date not null,
    foreign key (club_id) references club(id),
    foreign key (user_id) references users(id)
);

drop table if exists event cascade;
create table event (
    id serial primary key,
    club_id integer not null,
    host_id integer not null,
    date date not null,
    sinopsis text not null,
    contact varchar(255) not null,
    speaker varchar(255) not null,
    foreign key (club_id) references club(id),
    foreign key (host_id) references users(id)
);

drop table if exists event_reg cascade;
create table event_reg (
    id serial primary key,
    user_id integer not null,
    event_id integer not null,
    confirm bool not null, -- default false
    reg_date date not null,
    foreign key (user_id) references users(id),
    foreign key (event_id) references event(id)
);

drop table if exists mentorship cascade;
create table mentorship (
    id serial primary key,
    mentor_id integer not null,
    mentee_id integer not null,
    club_id integer not null,
    start_date date not null,
    end_date date not null,
    foreign key (mentor_id) references users(id),
    foreign key (mentee_id) references users(id),
    foreign key (club_id) references club(id)
);

drop table if exists achievement cascade;
create table achievement (
    id serial primary key,
    info text
);

drop table if exists user_x_achievement cascade;
create table user_x_achievement (
    id serial primary key,
    user_id integer not null,
    achievement_id integer not null,
    info text,
    foreign key (user_id) references users(id),
    foreign key (achievement_id) references achievement(id)
);

drop table if exists questionnaire cascade;
create table questionnaire (
    id serial primary key,
    user_id integer not null,
    info text,
    foreign key (user_id) references users(id)
);

drop table if exists randomcoffee cascade;
create table randomcoffee (
    id serial primary key,
    user_id1 integer not null,
    user_id2 integer not null,
    club_id integer not null,
    meet_date date not null,
    info text,
    foreign key (user_id1) references users(id),
    foreign key (user_id2) references users(id),
    foreign key (club_id) references club(id)
);
