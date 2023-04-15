import { useEffect, useState } from "react";
import Layout from "../../components/Layout";
import { observer } from "mobx-react";
import { addAnimalType, getAnimalTypes } from "../../models/animalTypeRequest";
import animalTypeStore from "../../store/animalTypes";
import {
  Box,
  Button,
  Card,
  CardBody,
  CardHeader,
  Heading,
  Input,
  Modal,
  ModalBody,
  ModalCloseButton,
  ModalContent,
  ModalHeader,
  ModalOverlay,
  Stack,
  StackDivider,
} from "@chakra-ui/react";
import styles from "./main.module.scss";
import { SubmitHandler, useForm } from "react-hook-form";
import * as yup from "yup";
import { yupResolver } from "@hookform/resolvers/yup";

type InputType = {
  type: string;
};

function AnimalTypes() {
  const [errorMsg, setErrorMsg] = useState("");
  const [openModal, setOpenModal] = useState(false);

  const openModalHandler = () => {
    setOpenModal(true);
  };
  const closeModalHandler = () => {
    setOpenModal(false);
  };

  useEffect(() => {
    getAnimalTypes().then((val) =>
      typeof val === "string"
        ? setErrorMsg(val)
        : (animalTypeStore.animalType = val)
    );
  }, []);

  const validationSchema = yup.object({
    type: yup.string().required("Данное поле обязательно"),
  });

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<InputType>({ resolver: yupResolver(validationSchema) });
  const onSubmit: SubmitHandler<InputType> = async (data) => {
    await addAnimalType(data).then((val) =>
      typeof val === "string"
        ? setErrorMsg(val)
        : (animalTypeStore.animalType = [...animalTypeStore.animalType!, val])
    );
    setOpenModal(false);
    reset();
  };

  return (
    <Layout>
      <div className={styles.topBlock}>
        <Button
          backgroundColor="green.300"
          _hover={{ backgroundColor: "green.400" }}
          onClick={openModalHandler}
        >
          Добавить тип животного
        </Button>
      </div>
      <div className={styles.main}>
        {animalTypeStore.animalType && animalTypeStore.animalType.length > 0 ? (
          <Card>
            <CardHeader>
              <Heading size="md">Типы животных:</Heading>
            </CardHeader>

            <CardBody>
              <Stack divider={<StackDivider />} spacing="4">
                {animalTypeStore.animalType?.map((type) => (
                  <Box key={type.id}>
                    <Heading size="xs" textTransform="uppercase">
                      {type.type}
                    </Heading>
                  </Box>
                ))}
              </Stack>
            </CardBody>
          </Card>
        ) : (
          <Card>
            <CardHeader>
              <Heading size="md">
                Пока что нет ни одного типа животного...{" "}
              </Heading>
            </CardHeader>
          </Card>
        )}
      </div>
      {errorMsg.length > 0 && (
        <div className={styles.noAnimals}>{errorMsg}</div>
      )}
      <Modal isOpen={openModal} onClose={closeModalHandler} isCentered>
        <ModalOverlay />
        <ModalContent padding={5}>
          <ModalHeader>Добавление нового типа животного</ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            <form onSubmit={handleSubmit(onSubmit)}>
              <Stack spacing={3}>
                <Input
                  placeholder="Введите тип животного"
                  {...register("type")}
                />
                {errors.type && (
                  <span className={styles.errorMessage}>
                    {errors.type?.message}
                  </span>
                )}
                <Button
                  backgroundColor={"green.700"}
                  _hover={{ backgroundColor: "green.800" }}
                  color={"white"}
                  type="submit"
                >
                  Добавить
                </Button>
              </Stack>
            </form>
          </ModalBody>
        </ModalContent>
      </Modal>
    </Layout>
  );
}

export default observer(AnimalTypes);
