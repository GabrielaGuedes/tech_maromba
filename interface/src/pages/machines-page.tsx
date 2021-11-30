import React, { useEffect, useState } from "react";
import { getMachines } from "../utils/endpoints";
import MachineCard from "./machine-card";
import bell from "../bell-regular.svg";
import NotificationsModal from "./notifications-modal";

interface IMachinesPage {}

const MachinesPage: React.FC<IMachinesPage> = () => {
  const [machines, setMachines] = useState<any>([]);
  const [isNotificationsOpen, setIsNotificationsOpen] = useState(false);

  useEffect(() => {
    getMachines().then((res) => {
      setMachines(res);
    });
  }, []);

  return (
    <div style={{ textAlign: "center" }}>
      <NotificationsModal
        isOpen={isNotificationsOpen}
        setIsOpen={setIsNotificationsOpen}
      />
      <div
        style={{
          display: "flex",
          justifyContent: "flex-end",
          width: 300,
          marginLeft: "auto",
          marginRight: "auto",
          marginTop: "20px",
        }}
        onClick={() => setIsNotificationsOpen(true)}
      >
        <img src={bell} height={30} alt="Notificações" />
      </div>
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          width: "100%",
          alignItems: "center",
          marginTop: 20,
        }}
      >
        {machines?.length > 0 &&
          machines.map((m: any) => <MachineCard id={m[0]} name={m[1]} />)}
      </div>
    </div>
  );
};

export default MachinesPage;
