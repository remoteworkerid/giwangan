INSERT INTO public.role(
            id, name)
    VALUES (1, 'admin');

INSERT INTO public.roles_users(
            user_id, role_id)
    VALUES (1, 1);

