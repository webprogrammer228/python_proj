import {
  Button,
  FormControl,
  FormLabel,
  Input,
  InputGroup,
  InputRightElement,
  Link,
  Modal,
  ModalBody,
  ModalContent,
  ModalHeader,
  ModalOverlay,
  Stack,
} from "@chakra-ui/react";
import styles from "./main.module.scss";
import { SubmitHandler, useForm } from "react-hook-form";
import * as yup from "yup";
import { yupResolver } from "@hookform/resolvers/yup";
import $api from "../../api/instance";
import { useCallback, useEffect, useState } from "react";
import { observer } from "mobx-react";
import { useNavigate } from "react-router-dom";

type Inputs = {
  firstName: string;
  lastName: string;
  email: string;
  password: string;
};

function Registration() {
  const [errorMessage, setErrorMessage] = useState("");
  const [show, setShow] = useState(false);
  const handleClick = () => setShow(!show);
  const [showModal, setShowModal] = useState(false);

  const validationSchema = yup.object({
    firstName: yup.string().max(255).required("Данное поле обязательно"),
    lastName: yup.string().max(255).required("Данное поле обязательно"),
    email: yup
      .string()
      .email("Невалидный почтовый адрес")
      .required("Данное поле обязательно"),
    password: yup.string().required("Данное поле обязательно"),
  });

  const navigate = useNavigate();

  const modalClose = useCallback(() => {
    setTimeout(() => {
      setShowModal(false);
      navigate({ pathname: "/" });
    }, 3000);
  }, [navigate]);

  useEffect(() => {
    if (showModal) {
      modalClose();
    }
  }, [showModal, modalClose]);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<Inputs>({ resolver: yupResolver(validationSchema) });
  const onSubmit: SubmitHandler<Inputs> = (data) =>
    $api
      .post("registration", data)
      .then(() => {
        setErrorMessage("");
        setShowModal(true);
      })
      .catch((e) => setErrorMessage(e.response.data.message));
  return (
    <div className={styles.main}>
      <form onSubmit={handleSubmit(onSubmit)} className={styles.form}>
        <h1 className={styles.title}>Чипизация животных</h1>
        <Stack spacing={3} width={500}>
          <FormLabel>Регистрация</FormLabel>
          <FormControl isInvalid={!!errors.firstName?.message}>
            <Input
              placeholder="Введите имя"
              size="lg"
              {...register("firstName")}
            />

            {errors.firstName && (
              <span className={styles.errorMessage}>
                {errors.firstName?.message}
              </span>
            )}
          </FormControl>
          <FormControl isInvalid={!!errors.lastName?.message}>
            <Input
              placeholder="Введите фамилию"
              size="lg"
              {...register("lastName")}
            />

            {errors.lastName && (
              <span className={styles.errorMessage}>
                {errors.lastName?.message}
              </span>
            )}
          </FormControl>
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
            Зарегистрироваться
          </Button>
          {errorMessage && (
            <span className={styles.errorMessage}>{errorMessage}</span>
          )}
          <p>
            Есть аккаунт?{" "}
            <Link color={"blue.500"} href="/">
              Вход
            </Link>
          </p>
        </Stack>
      </form>
      <Modal isOpen={showModal} onClose={modalClose}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Спасибо за регистрацию!</ModalHeader>
          <ModalBody>
            Мы переместим вас на страницу входа в течение 3 секунд
          </ModalBody>
        </ModalContent>
      </Modal>
    </div>
  );
}

export default observer(Registration);
