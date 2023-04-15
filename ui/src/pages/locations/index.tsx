import { useEffect, useState } from "react";
import Layout from "../../components/Layout";
import { addNewLocation, getLocations } from "../../models/locationsRequest";
import locationsStore from "../../store/locationsStore";
import styles from "./main.module.scss";
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
import * as yup from "yup";
import { observer } from "mobx-react";
import { SubmitHandler, useForm } from "react-hook-form";
import { yupResolver } from "@hookform/resolvers/yup";

type InputType = {
  longitude: number;
  latitude: number;
};

function Locations() {
  const [errorMsg, setErrorMsg] = useState("");
  const [openModal, setOpenModal] = useState(false);

  const openModalHandler = () => {
    setOpenModal(true);
  };
  const closeModalHandler = () => {
    setOpenModal(false);
  };

  useEffect(() => {
    getLocations().then((val) =>
      typeof val === "string"
        ? setErrorMsg(val)
        : (locationsStore.locations = val)
    );
  }, []);

  const validationSchema = yup.object({
    latitude: yup
      .number()
      .typeError("Только числа")
      .required("Данное поле обязательно")
      .min(-90, "Широта не менее -90")
      .max(90, "Широта не более 90"),
    longitude: yup
      .number()
      .typeError("Только числа")
      .required("Данное поле обязательно")
      .min(-180, "Долгота не менее -180")
      .max(180, "Долгота не более 180"),
  });

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<InputType>({ resolver: yupResolver(validationSchema) });
  const onSubmit: SubmitHandler<InputType> = async (data) => {
    console.log(data);
    await addNewLocation(data).then((val) =>
      typeof val === "string"
        ? setErrorMsg(val)
        : (locationsStore.locations = [...locationsStore.locations!, val])
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
          Добавить новую точку локации
        </Button>
      </div>
      <div className={styles.main}>
        {locationsStore.locations && locationsStore.locations.length > 0 ? (
          <Card>
            <CardHeader>
              <Heading size="md">Локации:</Heading>
            </CardHeader>

            <CardBody>
              <Stack divider={<StackDivider />} spacing="4">
                {locationsStore.locations?.map((location) => (
                  <Box key={location.id}>
                    <Heading size="xs" textTransform="uppercase">
                      Широта - {location.latitude}
                    </Heading>
                    <Heading size="xs" textTransform="uppercase">
                      Долгота - {location.longitude}
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
                Пока что нет ни одной точки локации...{" "}
              </Heading>
            </CardHeader>
          </Card>
        )}
      </div>

      {errorMsg.length > 0 && (
        <div className={styles.noLocations}>{errorMsg}</div>
      )}
      <Modal isOpen={openModal} onClose={closeModalHandler} isCentered>
        <ModalOverlay />
        <ModalContent padding={5}>
          <ModalHeader>Добавление нового типа животного</ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            <form onSubmit={handleSubmit(onSubmit)}>
              <Stack spacing={3}>
                <Input placeholder="Введите широту" {...register("latitude")} />
                {errors.latitude && (
                  <span className={styles.errorMessage}>
                    {errors.latitude?.message}
                  </span>
                )}
                <Input
                  placeholder="Введите долготу"
                  {...register("longitude")}
                />
                {errors.longitude && (
                  <span className={styles.errorMessage}>
                    {errors.longitude?.message}
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

export default observer(Locations);
