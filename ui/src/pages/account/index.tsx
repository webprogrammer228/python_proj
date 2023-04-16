import { useEffect } from "react";
import Layout from "../../components/Layout";
import accountRequest from "../../models/accountRequest";
import { observer } from "mobx-react";
import auth from "../../store/authStore";
import {
  Box,
  Card,
  CardBody,
  CardHeader,
  Heading,
  Stack,
  StackDivider,
  Text,
} from "@chakra-ui/react";

function Account() {
  useEffect(() => {
    accountRequest().then((val) => {
      auth.email = val.data.email;
      auth.firstName = val.data.firstName;
      auth.lastName = val.data.lastName;
      auth.id = val.data.id;
    });
  }, []);

  return (
    <Layout>
      <Card>
        <CardHeader>
          <Heading size="lg">Информация об аккаунте</Heading>
        </CardHeader>

        <CardBody>
          <Stack divider={<StackDivider />} spacing="4">
            <Box>
              <Heading size="md" textTransform="uppercase">
                Id:
              </Heading>
              {
                <Text pt="2" fontSize="lg">
                  {auth.id}
                </Text>
              }
            </Box>
            <Box>
              <Heading size="md" textTransform="uppercase">
                Имя:
              </Heading>

              <Text pt="2" fontSize="lg">
                {auth.firstName}
              </Text>
            </Box>
            <Box>
              <Heading size="md" textTransform="uppercase">
                Фамилия:
              </Heading>
              <Text pt="2" fontSize="lg">
                {auth.lastName}
              </Text>
            </Box>
            <Box>
              <Heading size="md" textTransform="uppercase">
                Электронная почта:
              </Heading>
              <Text pt="2" fontSize="lg">
                {auth.email}
              </Text>
            </Box>
          </Stack>
        </CardBody>
      </Card>
    </Layout>
  );
}

export default observer(Account);
