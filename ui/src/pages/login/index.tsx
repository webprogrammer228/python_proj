import {
  Button,
  FormControl,
  FormLabel,
  Input,
  InputGroup,
  InputRightElement,
  Link,
  Stack,
} from "@chakra-ui/react";
import styles from "./main.module.scss";
import { SubmitHandler, useForm } from "react-hook-form";
import * as yup from "yup";
import { yupResolver } from "@hookform/resolvers/yup";
import { useState } from "react";
import { observer } from "mobx-react";
import { useNavigate } from "react-router-dom";
import loginRequest from "../../models/loginRequest";

type Inputs = {
  email: string;
  password: string;
};

function Login() {
  const [errorMessage, setErrorMessage] = useState("");
  const [show, setShow] = useState(false);
  const handleClick = () => setShow(!show);

  const navigate = useNavigate();

  const validationSchema = yup.object({
    email: yup
      .string()
      .email("Невалидный почтовый адрес")
      .required("Данное поле обязательно"),
    password: yup.string().required("Данное поле обязательно"),
  });

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<Inputs>({ resolver: yupResolver(validationSchema) });
  const onSubmit: SubmitHandler<Inputs> = async (data) => {
    await loginRequest(data, { setErrorMessage, navigate });
  };

  return (
    <div className={styles.main}>
      <form onSubmit={handleSubmit(onSubmit)} className={styles.form}>
        <h1 className={styles.title}>Чипизация животных</h1>
        <Stack spacing={3} width={500}>
          <FormLabel>Вход</FormLabel>
          <FormControl isInvalid={!!errors.email?.message}>
            <Input
              placeholder="Введите электронную почту"
              size="lg"
              {...register("email")}
            />

            {errors.email && (
              <span className={styles.errorMessage}>
                {errors.email?.message}
              </span>
            )}
          </FormControl>
          <FormControl isInvalid={!!errors.password?.message}>
            <InputGroup size="lg">
              <Input
                pr="4.5rem"
                type={show ? "text" : "password"}
                placeholder="Введите пароль"
                {...register("password")}
              />
              <InputRightElement width="4.5rem">
                <Button h="1.75rem" size="sm" onClick={handleClick}>
                  {show ? "Hide" : "Show"}
                </Button>
              </InputRightElement>
            </InputGroup>
            {errors.password && (
              <span className={styles.errorMessage}>
                {errors.password?.message}
              </span>
            )}
          </FormControl>
          <Button type="submit" colorScheme="teal">
            Войти
          </Button>
          {errorMessage && (
            <span className={styles.errorMessage}>{errorMessage}</span>
          )}
          <p>
            Нет аккаунта?{" "}
            <Link color={"blue.500"} href="/registration">
              Регистрация
            </Link>
          </p>
        </Stack>
      </form>
    </div>
  );
}

export default observer(Login);
