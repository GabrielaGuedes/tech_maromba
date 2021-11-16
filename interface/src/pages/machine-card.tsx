import { Button, Card } from "antd";
import React, { Fragment, useEffect, useState } from "react";
import { getQueue } from "../utils/endpoints";

interface IMachineCard {
  name: string;
  id: string;
}

const MachineCard: React.FC<IMachineCard> = ({ id, name }) => {
  const [queue, setQueue] = useState<any>();

  useEffect(() => {
    getQueue(id).then((res) => {
      setQueue(res);
    });
  }, []);

  return (
    <Card
      title={name}
      bordered
      style={{ width: 300, border: "1px solid black", marginBottom: 10 }}
    >
      <Button type="primary">Se inserir na fila</Button>
      <div>Há {queue?.length} pessoas na fila.</div>
    </Card>
  );
};

export default MachineCard;
