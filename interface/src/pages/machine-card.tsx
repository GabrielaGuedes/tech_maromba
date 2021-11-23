import { Button, Card, InputNumber, Modal, Space } from "antd";
import { valueType } from "antd/lib/statistic/utils";
import React, { useEffect, useState } from "react";
import { CONSTANTS } from "../utils/constants";
import { getQueue, insertInQueue } from "../utils/endpoints";

interface IMachineCard {
  name: string;
  id: string;
}

const MachineCard: React.FC<IMachineCard> = ({ id, name }) => {
  const [queue, setQueue] = useState<any>();
  const [userQueuePosition, setUserQueuePosition] = useState<any>();
  const [isModalVisible, setIsModalVisible] = useState<boolean>(false);
  const [seriesNumber, setSeriesNumber] = useState<number>();
  const [repetitionsNumber, setRepetitionsNumber] = useState<number>();

  useEffect(() => {
    getQueue(id).then((res) => {
      setQueue(res);

      const position = res.findIndex((q: any) => q[3] === CONSTANTS.userId);
      if (position !== -1) {
        setUserQueuePosition(position + 1);
        console.log(position);
      }
    });
  }, []);

  const updateQueue = () => {
    getQueue(id).then((res) => {
      setQueue(res);

      const position = res.findIndex((q: any) => q[3] === CONSTANTS.userId);
      if (position) {
        setUserQueuePosition(position + 1);
      }
    });
  };

  const handleOk = () => {
    if (!seriesNumber || !repetitionsNumber) {
      alert("Preencha todos os campos!");
    } else {
      insertInQueue(id, CONSTANTS.userId, seriesNumber, repetitionsNumber).then(
        (res) => {
          if (res.result.includes("Success")) {
            alert("Inserido na fila!");
            updateQueue();
            setIsModalVisible(false);
          } else {
            alert("Ops, algo deu errado. Tente novamente.");
          }
        }
      );
    }
  };

  return (
    <Card
      title={name}
      bordered
      style={{ width: 300, border: "1px solid black", marginBottom: 10 }}
    >
      <Button type="primary" onClick={() => setIsModalVisible(true)}>
        Se inserir na fila
      </Button>
      <Modal
        title={`Fila - ${name}`}
        visible={isModalVisible}
        onCancel={() => setIsModalVisible(false)}
        onOk={handleOk}
      >
        Digite as séries e repetições:
        <Space style={{ marginLeft: "8px" }}>
          <InputNumber
            placeholder="4"
            value={seriesNumber as valueType}
            onChange={(value) => setSeriesNumber(value as number)}
          />
          x
          <InputNumber
            placeholder="15"
            value={repetitionsNumber as valueType}
            onChange={(value) => setRepetitionsNumber(value as number)}
          />
        </Space>
      </Modal>
      <div>Há {queue?.length} pessoas na fila.</div>
      {userQueuePosition > 0 && <div>Sua posição é a {userQueuePosition}.</div>}
    </Card>
  );
};

export default MachineCard;
