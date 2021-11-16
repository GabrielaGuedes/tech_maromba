import { getRequest, postRequest } from "./requests";

const baseUrl = process.env.REACT_APP_CENTRAL_SERVER_API;

export const getMachines = async () => {
  return await getRequest(baseUrl + "/machines");
};

export const getQueue = async (id) => {
  return await getRequest(baseUrl + "/queue/" + id);
};

export const getPositionInQueue = async (machineId, userId) => {
  return await getRequest(baseUrl + "/queue/" + machineId + "/" + userId);
};

export const insertInQueue = async (machineId, userId, series, repetitions) => {
  const body = {
    machine_id: machineId,
    user_id: userId,
    series,
    repetitions,
  };

  return await postRequest(baseUrl + "/queue/insert", body);
};

export const getNotifications = async (userId) => {
  return await getRequest(baseUrl + "/notifications/" + userId);
};

export const userArrived = async (machineId, userId) => {
  return await postRequest(
    baseUrl + "/queue/user_arrived/" + userId + machineId
  );
};
