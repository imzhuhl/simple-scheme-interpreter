
def extend_env(var, val, old_env):
    old_env.append((var, val))
    print(id(old_env))
    return old_env

def main():
    env = []
    print(id(env))
    env = extend_env("a", 10, env)
    print(env)


if __name__ == '__main__':
    main()