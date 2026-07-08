export interface Contract {
  id: number;
  template_id: string;
  customer_name: string;
  city: string;
  state: string;
  start_date: string;
  end_date: string;
  contract_price: string;
  created_at: string | null;
}

export interface ContractData {
  template_id: string;
  customer_name: string;
  city: string;
  state: string;
  start_date: string;
  end_date: string;
  contract_price: string;
}
