import { FormEvent, useEffect, useState } from "react";
import Layout from "../../components/Layout";
import { getAnimal, addAnimal } from "../../models/animalsRequest";
import animalStore from "../../store/animalStore";
import styles from "./main.module.scss";
import {
  Button,
  Input,
  Modal,
  ModalBody,
  ModalCloseButton,
  ModalContent,
  ModalHeader,
  ModalOverlay,
  Stack,
  Select,
  Card,
  CardHeader,
  Heading,
  CardBody,
  StackDivider,
  Box,
} from "@chakra-ui/react";
import { observer } from "mobx-react";
import locationsStore from "../../store/locationsStore";
import auth from "../../store/authStore";
import { getLocations } from "../../models/locationsRequest";
import { getAnimalTypes } from "../../models/animalTypeRequest";
import animalTypeStore from "../../store/animalTypesStore";
import { Select as MultipleSelect } from "chakra-react-select";

function Animal() {
  const [errorMsg, setErrorMsg] = useState("");
  const [openModal, setOpenModal] = useState(false);
  const [animalType, setAnimalType] = useState<number[]>([]);
  const [weight, setWeight] = useState<number>(0);
  const [length, setLength] = useState<number>(0);
  const [height, setHeight] = useState<number>(0);
  const [gender, setGender] = useState("");
  const [chippingLocationId, setChippingLocationId] = useState<number>(0);

  const options = [
    {
      label: "Типы животных",
      options: animalTypeStore.animalType
        ? animalTypeStore.animalType.map((animal) => {
            return { value: animal.id, label: animal.type };
          })
        : [{ value: "null", label: "some" }],
    },
  ];

  const openModalHandler = () => {
    setOpenModal(true);
  };
  const closeModalHandler = () => {
    setOpenModal(false);
  };

  useEffect(() => {
    getAnimal().then((val) =>
      typeof val === "string" ? setErrorMsg(val) : (animalStore.animal = val)
    );
    getLocations().then((val) =>
      typeof val === "string"
        ? setErrorMsg(val)
        : (locationsStore.locations = val)
    );
    getAnimalTypes().then((val) =>
      typeof val === "string"
        ? setErrorMsg(val)
        : (animalTypeStore.animalType = val)
    );
  }, []);

  const onSubmit = async (e: FormEvent) => {
    e.preventDefault();
    await addAnimal({
      animalTypes: animalType,
      weight: weight,
      length: length,
      height: height,
      gender: gender,
      chipperId: Number(auth.id),
      chippingLocationId: chippingLocationId,
    }).then((val) =>
      typeof val === "string"
        ? setErrorMsg(val)
        : (animalStore.animal = [...animalStore.animal, val])
    );
    closeModalHandler();
  };

  return (
    <Layout>
      <div className={styles.topBlock}>
        <Button
          backgroundColor="green.300"
          _hover={{ backgroundColor: "green.400" }}
          onClick={openModalHandler}
        >
          Добавить животное
        </Button>
      </div>
      {errorMsg.length > 0 && (
        <div className={styles.noAnimals}>
          Нет ни одного животного, которое вы отслеживаете
        </div>
      )}
      {errorMsg.length === 0 && (
        <div className={styles.content}>
          <Card>
            <CardHeader>
              <Heading size="md">Животные:</Heading>
            </CardHeader>

            <CardBody>
              <Stack divider={<StackDivider />} spacing="4">
                {animalStore.animal &&
                  animalStore.animal.map((animal) => (
                    <Box key={animal.id}>
                      <Heading size="xs" textTransform="uppercase">
                        Вес животного - {animal.weight} кг.
                      </Heading>
                      <Heading size="xs" textTransform="uppercase">
                        Длина животного - {animal.length} м.
                      </Heading>
                      <Heading size="xs" textTransform="uppercase">
                        Высота животного - {animal.height} м.
                      </Heading>
                      <Heading size="xs" textTransform="uppercase">
                        Пол животного -{" "}
                        {animal.gender === "MALE"
                          ? "Мужской"
                          : animal.gender === "FEMALE"
                          ? "Женский"
                          : "Другой"}
                      </Heading>
                      <Heading size="xs" textTransform="uppercase">
                        Состояние жизни -{" "}
                        {animal.lifeStatus === "ALIVE" ? "Живой" : "Мертв"}
                      </Heading>
                      <Heading size="xs" textTransform="uppercase">
                        Посещенные локации -{" "}
                        {animal.visitedLocations.length > 0
                          ? animal.visitedLocations.map((visitedLocations) => (
                              <span>{visitedLocations}</span>
                            ))
                          : "Отсутствуют"}
                      </Heading>
                      {animal.deathDateTime !== null && (
                        <Heading size="xs" textTransform="uppercase">
                          Время смерти - {animal.deathDateTime}
                        </Heading>
                      )}
                      <Heading size="xs" textTransform="uppercase">
                        Время чипирования -{" "}
                        {new Date(animal.chippingDateTime).toLocaleString()}
                      </Heading>
                    </Box>
                  ))}
              </Stack>
            </CardBody>
          </Card>
        </div>
      )}

      <Modal isOpen={openModal} onClose={closeModalHandler} isCentered>
        <ModalOverlay />
        <ModalContent padding={5}>
          <ModalHeader>Добавление нового животного</ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            <form onSubmit={onSubmit}>
              <Stack spacing={3}>
                <MultipleSelect
                  isMulti
                  placeholder="Выберите один или несколько типов животных"
                  options={options}
                  onChange={(e) => {
                    const allTypesIndex = e.reduce(
                      (acc: number[], prevVal: any) => {
                        return [...acc, prevVal.value];
                      },
                      []
                    );
                    setAnimalType(allTypesIndex);
                  }}
                />

                <Input
                  placeholder="Введите вес животного(в килограммах)"
                  onChange={(e) => setWeight(Number(e.target.value))}
                  type="number"
                />
                <Input
                  placeholder="Введите длину животного(в метрах)"
                  onChange={(e) => setLength(Number(e.target.value))}
                  type="number"
                />
                <Input
                  placeholder="Введите высоту животного(в метрах)"
                  onChange={(e) => setHeight(Number(e.target.value))}
                  type="number"
                />
                <Select
                  placeholder="Выберите пол животного"
                  onChange={(e) => setGender(e.target.value)}
                >
                  <option value="MALE">Мужской</option>
                  <option value="FEMALE">Женский</option>
                  <option value="OTHER">Другой</option>
                </Select>
                <Input value={auth.id} onChange={() => false} />
                <Select
                  placeholder="Выберите локацию животного"
                  onChange={(e) =>
                    setChippingLocationId(Number(e.target.value))
                  }
                >
                  {locationsStore.locations.map((location) => (
                    <option key={location.id} value={location.id}>
                      {location.latitude + " " + location.longitude}
                    </option>
                  ))}
                </Select>
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

export default observer(Animal);
